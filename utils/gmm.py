from typing import Any

def gmm(
    lhs: jnp.ndarray,
    rhs: jnp.ndarray,
    group_sizes: jnp.ndarray,
    preferred_element_type: jnp.dtype = jnp.float32,
    tiling: tuple[int, int, int] | LutFn | None = (128, 128, 128),
    group_offset: jnp.ndarray | None = None,
    existing_out: jnp.ndarray | None = None,
    transpose_rhs: bool = False,
    interpret: bool = False,
) -> jnp.ndarray:
  """Compute lhs[sizes[i-1]:sizes[i], :] @ rhs for each group 'i'.

  Args:
    lhs: A 2d, jnp.ndarray with shape [m, k].
    rhs: A 3d, jnp.ndarray with shape [num_groups, k, n].
    group_sizes: A 1d, jnp.ndarray with shape [num_groups] and jnp.int32 dtype.
    preferred_element_type: jnp.dtype, the element type for the output matrix.
    tiling: 3-tuple of ints. The m, k and n-dimension tile sizes.
    group_offset: The group in group sizes to start computing from. This is
      particularly useful for when rhs num_groups is sharded.
    existing_out: Existing output to write to.
    transpose_rhs: True if the rhs needs to be transposed.
    interpret: Whether or not to run the kernel in interpret mode, helpful for
      testing and debugging.

  Returns:
    A 2d, jnp.ndarray with shape [m, n].
  """

  if existing_out is not None:
    assert isinstance(existing_out, jax.Array)
    expected_dtype = existing_out.dtype
    if expected_dtype != preferred_element_type:
      raise ValueError(
          "Existing output dtype must match preferred_element_type."
      )
  if group_offset is None:
    group_offset = jnp.array([0], dtype=jnp.int32)
  else:
    if group_offset.shape:
      raise ValueError(
          f"group_offset must be a ()-shaped array. Got: {group_offset.shape}."
      )
    group_offset = group_offset[None]
  num_current_groups = rhs.shape[0]
  num_total_groups = group_sizes.shape[0]
  lhs, group_sizes, input_dtype = _validate_args(
      lhs=lhs, rhs=rhs, group_sizes=group_sizes
  )

  # Gather shape information.
  m, k, n = (lhs.shape[0], lhs.shape[1], rhs.shape[2])
  if transpose_rhs:
    n = rhs.shape[1]

  # If tiling is callable, look up the problem dimensions in the LUT. If no tuned
  # tile dimensions are available throw an error.
  if callable(tiling):
    tiling = tiling(m, k, n)

  if tiling is None:
    raise ValueError(f"No tuned tiling found for (m, k, n) = ({m}, {k}, {n})")

  tm, tk, tn = tiling
  tiles_k, k_rem = _calculate_irregular_num_tiles(k, tk)
  tiles_n, n_rem = _calculate_irregular_num_tiles(n, tn)
  del n_rem

  # Create the metadata we need for computation.
  group_metadata, num_active_tiles = make_group_metadata(
      group_sizes=group_sizes,
      m=m,
      tm=tm,
      start_group=group_offset[0],
      num_nonzero_groups=rhs.shape[0],
      visit_empty_groups=False,
  )

  def kernel(
      group_metadata,
      group_offset,
      lhs,
      rhs,
      existing_out,
      out,
      acc_scratch,
  ):
    group_offsets, group_ids, m_tile_ids = group_metadata
    del group_offsets, group_ids, group_offset

    grid_id = pl.program_id(1)
    k_i = pl.program_id(2)

    @pl.when(k_i == 0)
    def _zero_acc():
      acc_scratch[...] = jnp.zeros_like(acc_scratch)

      if existing_out is not None:
        prev_grid_id = jnp.where(grid_id > 0, grid_id - 1, 0)
        is_first_processed_group = grid_id == 0
        m_tile_changed = m_tile_ids[grid_id] != m_tile_ids[prev_grid_id]
        first_time_seeing_out = jnp.logical_or(
            is_first_processed_group, m_tile_changed
        )

        @pl.when(first_time_seeing_out)
        def _init_out():
          out[...] = existing_out[...]

    def mask_k_rem(x, *, dim):
      if k_rem == 0:
        return x

      orig_dtype = x.dtype
      iota = lax.broadcasted_iota(jnp.int32, x.shape, dim)
      x = x.astype(jnp.float32)
      return jnp.where(iota < k_rem, x, 0).astype(orig_dtype)

    def _store_accum():
      mask = _get_store_mask(
          grid_id=grid_id,
          group_metadata=group_metadata,
          tm=tm,
          tn=tn,
      )
      to_store = acc_scratch[...]
      out[...] = jax.lax.select(
          mask[...], to_store, out[...].astype(jnp.float32)
      ).astype(preferred_element_type)

    def _accum(is_last_k_tile):
      if is_last_k_tile:
        mask_k_rem_lhs = partial(mask_k_rem, dim=1)
        mask_k_rem_rhs = partial(mask_k_rem, dim=int(transpose_rhs))
      else:
        mask_k_rem_lhs = lambda x: x
        mask_k_rem_rhs = lambda x: x

      if transpose_rhs:
        dot_general_dims = (((1,), (1,)), ((), ()))
      else:
        dot_general_dims = (((1,), (0,)), ((), ()))

      loaded_lhs = lhs[...]
      loaded_rhs = rhs[...]
      acc_scratch[...] += lax.dot_general(
          mask_k_rem_lhs(loaded_lhs).astype(input_dtype),
          mask_k_rem_rhs(loaded_rhs).astype(input_dtype),
          preferred_element_type=jnp.float32,
          dimension_numbers=dot_general_dims,
      )

      if is_last_k_tile:
        _store_accum()

    lax.cond(
        k_i == tiles_k - 1,
        partial(_accum, True),
        partial(_accum, False),
    )

  def lhs_transform_indices(n_i, grid_id, k_i, group_metadata, group_offset):
    # lhs is (m, k). Load the [tm, tk] matrix for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del n_i, group_offsets, group_ids, group_offset
    return m_tile_ids[grid_id], k_i

  def rhs_transform_indices(n_i, grid_id, k_i, group_metadata, group_offset):
    # rhs is (num_groups, k, n). Load the [tk, tn] matrix based on the group id
    # for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del group_offsets, m_tile_ids
    if transpose_rhs:
      k_i, n_i = n_i, k_i

    # NOTE: If we're working on only a shard of the rhs we need to adjust the
    # group index we load from to account for this. The group_ids are in the
    # "unsharded" domain.
    return group_ids[grid_id] - group_offset[0], k_i, n_i

  def out_transform_indices(n_i, grid_id, k_i, group_metadata, group_offset):
    # out is (m, n). Load the [tm, tn] matrix for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del k_i, group_offsets, group_ids, group_offset
    return m_tile_ids[grid_id], n_i

  out_block_spec = pl.BlockSpec((tm, tn), out_transform_indices)
  if existing_out is None:
    in_out_block_spec: Any = None
    input_output_aliases = {}
  else:
    in_out_block_spec = out_block_spec
    input_output_aliases = {6: 0}

  lhs_block_spec = pl.BlockSpec((tm, tk), lhs_transform_indices)
  if transpose_rhs:
    rhs_block_spec = pl.BlockSpec((None, tn, tk), rhs_transform_indices)
  else:
    rhs_block_spec = pl.BlockSpec((None, tk, tn), rhs_transform_indices)

  lhs_bytes = lhs.size * lhs.itemsize
  rhs_bytes = (k * n) * rhs.itemsize  # We don't read all of rhs
  out_bytes = (m * n) * jnp.dtype(preferred_element_type).itemsize
  max_active_tiles = group_metadata[1].size
  bytes_accessed = (
      (lhs_bytes * tiles_n) + (rhs_bytes * max_active_tiles) + out_bytes
  )
  flops = 2 * m * k * n
  cost_estimate = pl.CostEstimate(
      flops=flops, bytes_accessed=bytes_accessed, transcendentals=0
  )
  call_gmm = pl.pallas_call(
      kernel,
      out_shape=jax.ShapeDtypeStruct((m, n), preferred_element_type),
      grid_spec=pltpu.PrefetchScalarGridSpec(
          num_scalar_prefetch=2,
          in_specs=[
              lhs_block_spec,
              rhs_block_spec,
              in_out_block_spec,
          ],
          out_specs=out_block_spec,
          grid=(tiles_n, num_active_tiles, tiles_k),
          scratch_shapes=[pltpu.VMEM((tm, tn), jnp.float32)],
      ),
      input_output_aliases=input_output_aliases,
      compiler_params=pltpu.CompilerParams(
              dimension_semantics=("parallel", "arbitrary", "arbitrary")),
      interpret=interpret,
      cost_estimate=cost_estimate,
  )

  out = call_gmm(
      group_metadata,
      group_offset,
      lhs,
      rhs,
      existing_out,
  )
  if existing_out is None and num_current_groups < num_total_groups:
    out = _zero_uninitialized_memory(
        out,
        start_group=group_offset[0],
        num_nonzero_groups=rhs.shape[0],
        group_metadata=group_metadata,
    )
  return out

