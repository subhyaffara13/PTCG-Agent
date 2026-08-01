
def tgmm(
    lhs: jnp.ndarray,
    rhs: jnp.ndarray,
    group_sizes: jnp.ndarray,
    preferred_element_type: jnp.dtype = jnp.float32,
    tiling: tuple[int, int, int] | LutFn | None = (128, 128, 128),
    group_offset: jnp.ndarray | None = None,
    num_actual_groups: int | None = None,
    existing_out: jnp.ndarray | None = None,
    interpret: bool = False,
) -> jnp.ndarray:
  """Compute lhs[:, sizes[i-1]:sizes[i]] @ rhs[sizes[i-1]:sizes[i], :].

  Args:
    lhs: A 2d, jnp.ndarray with shape [k, m].
    rhs: A 2d, jnp.ndarray with shape [m, n].
    group_sizes: A 1d, jnp.ndarray with shape [num_groups] and jnp.int32 dtype.
    preferred_element_type: jnp.dtype, the element type for the output matrix.
    tiling: 3-tuple of ints. The m, k and n-dimension tile sizes.
    group_offset: The group in group sizes to start computing from. This is
      particularly useful for when rhs num_groups is sharded.
    num_actual_groups: For when num_groups is sharded and we should only compute
      the groups that are local, starting from group_offset.
    existing_out: Existing output to write to.
    interpret: Whether or not to run the kernel in interpret mode, helpful for
      testing and debugging.

  Returns:
    A  3d, jnp.ndarray with shape [num_groups, k, n].
  """
  if group_offset is None:
    group_offset = jnp.array([0], dtype=jnp.int32)
  else:
    group_offset = group_offset[None]
  lhs, group_sizes, input_dtype = _validate_args(
      lhs=lhs, rhs=rhs, group_sizes=group_sizes, expected_rhs_dims=2
  )

  # Gather shape information.
  k, m, n = (lhs.shape[0], lhs.shape[1], rhs.shape[1])
  num_groups = group_sizes.shape[0]
  num_actual_groups = (
      num_actual_groups if num_actual_groups is not None else num_groups
  )

  # If tiling is callable, look up the problem dimensions in the LUT. If no tuned
  # tile dimensions are available throw an error.
  if callable(tiling):
    tiling = tiling(m, k, n)

  if tiling is None:
    raise ValueError(f"No tuned tiling found for (m, k, n) = ({m}, {k}, {n})")

  tm, tk, tn = tiling
  tiles_k, k_rem = _calculate_irregular_num_tiles(k, tk)
  del k_rem
  tiles_n, n_rem = _calculate_irregular_num_tiles(n, tn)
  del n_rem

  # Create the metadata we need for computation.
  group_metadata, num_active_tiles = make_group_metadata(
      group_sizes=group_sizes,
      m=m,
      tm=tm,
      start_group=group_offset[0],
      num_nonzero_groups=num_actual_groups,
      visit_empty_groups=True,
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
    grid_id = pl.program_id(2)
    group_offsets, group_ids, m_tile_ids = group_metadata
    del group_offsets, group_offset, m_tile_ids

    group = group_ids[grid_id]
    prev_grid_id = jnp.where(grid_id > 0, grid_id - 1, 0)
    prev_group = group_ids[prev_grid_id]

    group_has_changed = jnp.logical_or(grid_id == 0, prev_group != group)

    @pl.when(group_has_changed)
    def _zero_acc():
      acc_scratch[...] = jnp.zeros_like(acc_scratch)

    # We'll only do computation if our group has a nonzero number of rows in it.
    dont_skip = (
        _get_group_size(grid_id=grid_id, group_metadata=group_metadata) > 0
    )

    @pl.when(dont_skip)
    def _do():
      rhs_mask = _get_store_mask(
          grid_id=grid_id,
          group_metadata=group_metadata,
          tm=tm,
          tn=tn,
      )
      lhs_mask = _get_store_mask(
          grid_id=grid_id,
          group_metadata=group_metadata,
          tm=tm,
          tn=tk,
      )

      loaded_lhs = lhs[...]
      loaded_rhs = rhs[...]
      loaded_lhs = lax.select(
          lhs_mask[...],
          loaded_lhs.astype(jnp.float32),
          jnp.zeros_like(lhs, jnp.float32),
      ).swapaxes(0, 1)
      loaded_rhs = lax.select(
          rhs_mask[...],
          loaded_rhs.astype(jnp.float32),
          jnp.zeros_like(rhs, jnp.float32),
      )

      acc_scratch[...] += lax.dot(
          loaded_lhs.astype(input_dtype),
          loaded_rhs.astype(input_dtype),
          preferred_element_type=jnp.float32,
      )

    is_end_of_grid = grid_id == (pl.num_programs(2) - 1)
    next_grid_id = jnp.where(is_end_of_grid, grid_id, grid_id + 1)
    next_group = group_ids[next_grid_id]

    group_is_changing = jnp.logical_or(is_end_of_grid, group != next_group)

    @pl.when(group_is_changing)
    def _store_accum():
      to_store = acc_scratch[...]
      if existing_out is not None:
        to_store += existing_out[...].astype(jnp.float32)
      out[...] = to_store.astype(preferred_element_type)

  def lhs_transform_indices(n_i, k_i, grid_id, group_metadata, group_offset):
    # lhs is (m, k). Load the [tm, tk] matrix for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del n_i, group_offsets, group_ids, group_offset
    return m_tile_ids[grid_id], k_i

  def rhs_transform_indices(n_i, k_i, grid_id, group_metadata, group_offset):
    # rhs is (m, n). Load the [tm, tn] matrix for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del k_i, group_offsets, group_ids, group_offset
    return m_tile_ids[grid_id], n_i

  def out_transform_indices(n_i, k_i, grid_id, group_metadata, group_offset):
    # out is (num_groups, k, n). Load the [tk, tn] matrix based on the group id
    # for this m-tile.
    group_offsets, group_ids, m_tile_ids = group_metadata
    del group_offsets, m_tile_ids

    # NOTE: If we're working on only a shard of the output we need to adjust the
    # group index we load from to account for this. The group_ids are in the
    # "unsharded" domain.
    return group_ids[grid_id] - group_offset[0], k_i, n_i

  out_block_spec = pl.BlockSpec((None, tk, tn), out_transform_indices)
  if existing_out is None:
    in_out_block_spec: Any = None
    input_output_aliases = {}
  else:
    in_out_block_spec = out_block_spec
    input_output_aliases = {6: 0}

  lhs_block_spec = pl.BlockSpec((tm, tk), lhs_transform_indices)
  rhs_block_spec = pl.BlockSpec((tm, tn), rhs_transform_indices)

  lhs_bytes = lhs.size * lhs.itemsize
  rhs_bytes = rhs.size * rhs.itemsize
  out_bytewidth = jnp.dtype(preferred_element_type).itemsize
  out_bytes = (num_actual_groups * k * n) * out_bytewidth
  bytes_accessed = (
      (lhs_bytes * tiles_n) + (rhs_bytes * tiles_k) + out_bytes
  )
  flops = 2 * m * k * n
  cost_estimate = pl.CostEstimate(
      flops=flops, bytes_accessed=bytes_accessed, transcendentals=0
  )
  lhs = lhs.swapaxes(0, 1)
  call_gmm = pl.pallas_call(
      kernel,
      out_shape=jax.ShapeDtypeStruct(
          (num_actual_groups, k, n), preferred_element_type
      ),
      grid_spec=pltpu.PrefetchScalarGridSpec(
          num_scalar_prefetch=2,
          in_specs=[
              lhs_block_spec,
              rhs_block_spec,
              in_out_block_spec,
          ],
          out_specs=out_block_spec,
          grid=(tiles_n, tiles_k, num_active_tiles),
          scratch_shapes=[pltpu.VMEM((tk, tn), jnp.float32)],
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
  return out

