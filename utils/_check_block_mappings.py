
def _check_block_mappings(
    block_mappings: tuple[pallas_core.BlockMapping, ...],
    lowering_context: mlir.LoweringRuleContext,
    debug_info: jax_core.DebugInfo,
    kernel_type: tpu_core.CoreType,
) -> None:
  del lowering_context  # originally needed for forward compat
  for bm in block_mappings:
    dtype = bm.array_aval.dtype
    array_shape = bm.array_aval.shape
    if should_physicalize_dtype(dtype):
      physical_element_aval = jax_core.physical_element_aval(dtype)
      physical_dtype = physical_element_aval.dtype
      physical_array_shape = jax_core.physical_shape(array_shape, dtype)
      physical_block_shape = bm.block_shape + tuple(
          pallas_core.Blocked(i) for i in physical_element_aval.shape)
    else:
      physical_dtype = dtype
      physical_array_shape = array_shape
      physical_block_shape = bm.block_shape

    rank = len(physical_block_shape)
    # TODO(necula): add tests for SMEM blocks with trivial windowing
    # We support scalars too
    block_memory_space = bm.block_aval.memory_space
    if block_memory_space is None:
      block_memory_space = pallas_core.MemorySpace.DEFAULT
    memory_space = tpu_core.memory_space_to_tpu_memory_space(
        block_memory_space, kernel_type
    )
    if memory_space == tpu_core.MemorySpace.SMEM and bm.has_trivial_window():
      continue
    if memory_space == tpu_core.MemorySpace.SEMAPHORE:
      continue

    def err_details():
      return (f"Block spec for {bm.origin} in pallas_call {debug_info.func_src_info} "
              "has block shape "
              f"{physical_block_shape}, array shape {physical_array_shape}, "
              # TODO(necula): add index_map source location info
              f"and index_map {bm.index_map_jaxpr.jaxpr}, in "
              f"memory space {bm.block_aval.memory_space!r}."
              "\nSee details at https://docs.jax.dev/en/latest/pallas/grid_blockspec.html#pallas-blockspec")
    if rank < 1:
      raise ValueError(
          "The Pallas TPU lowering currently supports only blocks of "
          "rank >= 1. " + err_details())

    if (
        memory_space is ANY or memory_space == tpu_core.MemorySpace.HBM
    ) and not bm.has_trivial_window():
      raise ValueError(
          "The Pallas TPU lowering currently supports in memory space ANY "
          "only blocks having the same block shape as the array shape "
          "and a trivial index_map (returning all 0s)." + err_details())

    unmapped_bs = pallas_core._get_block_shape(physical_block_shape)
    bs0, as0 = unmapped_bs[-1], physical_array_shape[-1]
    if rank >= 2:
      bs1, as1 = unmapped_bs[-2], physical_array_shape[-2]
    else:
      bs1, as1 = 1, 1

    if rank >= 2:
      evenly_divisible = (
          (bs0 == as0 or bs0 % 128 == 0) and
          (bs1 == as1 or bs1 % 8 == 0)
      )
      if not evenly_divisible:
        extra_msg = ""
        if pallas_core.dynamic_shapes_export_enabled():
          extra_msg = (
              " In dynamic shape export - your kernel symbolic args must be"
              " annotated with constraints where the computation *after*"
              " applying any grid mapping is divisible by 8 and 128"
              " respectively. Ex: (mod(floordiv(m_dim, grid_size), 8) == 0))"
          )
        raise ValueError(
            "The Pallas TPU lowering currently requires that the last two "
            "dimensions of your block shape are divisible by 8 and 128 "
            "respectively, or be equal to the respective dimensions of the "
            "overall array. "
            + extra_msg
            + err_details()
        )
    else:
      assert rank == 1
      if bm.array_aval.dtype == jnp.bool_:
        bitwidth = dtypes.itemsize_bits(BOOL_MEMREF_TYPE)
      else:
        bitwidth = dtypes.itemsize_bits(physical_dtype)
      packing = 32 // bitwidth
      sublane_count = tpu_info.get_tpu_info().num_sublanes
      lane_count = tpu_info.get_tpu_info().num_lanes
      min_tiling = lane_count * packing
      chunk_size = sublane_count * lane_count
      feasible_block_size = (
          bs0 == as0
          or bs0 % chunk_size == 0
          or (bs0 >= min_tiling and (bs0 & (bs0 - 1)) == 0)  # power of 2
      )
      if not feasible_block_size:
        raise ValueError(
            "The Pallas TPU lowering currently requires that rank 1 block"
            " shapes, either 1) the first (and only) dimension of the block"
            " shape is equal to the first (and only) dimension of the array"
            " shape, or 2) the first (and only) dimension of the block shape"
            f" is a multiple of {chunk_size}, or 3) the first (and only)"
            " dimension of the block shape is a power of 2 and at least the"
            f" tiling size ({min_tiling} = 128 * (32 //"
            f" {dtypes.itemsize_bits(physical_dtype)})) of the array shape. "
            + err_details()
        )


def _check_block_mappings(
    block_mappings: Sequence[pallas_core.BlockMapping],
    debug_info: jax_core.DebugInfo,
) -> None:
  def err_details(bm: pallas_core.BlockMapping) -> str:
    return (
        f"Block spec for {bm.origin} in pallas_call {debug_info.func_src_info}"
        f" has block shape {bm.block_shape}, array shape"
        f" {bm.array_aval.shape},"
        # TODO(necula): add index_map source location info
        f" and index_map {bm.index_map_jaxpr.jaxpr} in"
        f" memory space {bm.transformed_block_aval.memory_space}."
        " See details at"
        " https://docs.jax.dev/en/latest/pallas/grid_blockspec.html#pallas-blockspec."
    )

  for bm in block_mappings:
    if (
        bm.transformed_block_aval.memory_space == gpu_core.GMEM
        and not bm.has_trivial_window()
    ):
      raise NotImplementedError(
          "Mosaic GPU lowering currently requires blocks in GMEM memory space "
          "to have same block shape as the array shape "
          "and a trivial index_map (returning all 0s).\n\n"
          + err_details(bm)
      )

    if any(isinstance(b, pallas_core.Element) for b in bm.block_shape):
      raise NotImplementedError(
          "Only Blocked indexing mode is supported in Mosaic GPU lowering.\n\n"
          + err_details(bm)
      )

    if bm.pipeline_mode is not None:
      raise NotImplementedError(
          "Pipeline mode is not supported in Mosaic GPU lowering.\n\n"
          + err_details(bm)
      )

