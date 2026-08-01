
def do_matmul(a_gmem,
              b_gmem,
              out_gmem,
              grid_indices: Sequence[jax.Array],
              wg_axis: str,
              collective_axes: tuple[str, ...],
              local_index: jax.Array | int,
              config: TuningConfig,
              group_info: ragged_dot_mgpu.GroupInfo,
              a_smem, b_smem, acc_tmem, acc_smem,
              a_tma_barrier, b_tma_barrier, store_done_barrier, mma_done_barrier,
              consumed_barrier
              ):
  """Compute a non-ragged matmul for a single output block."""
  dtype = out_gmem.dtype
  m, k = a_gmem.shape
  collective = config.collective
  tile_m, tile_n, tile_k = (config.tile_m, config.tile_n, config.tile_k)
  epilogue_tile_n = config.epilogue_tile_n
  max_concurrent_steps = config.max_concurrent_steps
  block_tile_m = tile_m
  if collective:
    tile_m *= 2
    tile_n *= 2
  k_iters = k // tile_k

  if collective:
    m_index, n_index, cluster_idx = grid_indices
    block_m_index = m_index * 2 + cluster_idx
    is_lead_block = cluster_idx == 0
  else:
    m_index, n_index = grid_indices
    cluster_idx = 0
    block_m_index = m_index
    is_lead_block = True
  wg_idx = lax.axis_index(wg_axis)
  collective_axis = collective_axes[0] if collective else None

  TMA_WARP = 0
  MMA_WARP = 1
  COMPUTE_WG = 0
  STORE_WG = 1

  block_slice_m = pl.ds(block_m_index * block_tile_m, block_tile_m)
  slice_m = pl.ds(m_index * tile_m, tile_m)
  slice_n = pl.ds(n_index * tile_n, tile_n)
  acc_slot = lax.rem(local_index, jnp.int32(2))
  regs_layout = plgpu.Layout.TCGEN05

  @pl.when(wg_idx == COMPUTE_WG)
  @jax.named_scope("compute_wg")
  def _():
    @pl.core_map(plgpu.WarpMesh(axis_name="warp"))
    def _per_warp():
      warp_id = lax.axis_index("warp")
      @pl.when(warp_id == TMA_WARP)
      def _memory():
        def _loop_body(ki, _):
          slice_k = pl.ds(ki * tile_k, tile_k)
          slot = lax.rem(ki, max_concurrent_steps)
          @pl.when(jnp.logical_or(ki >= max_concurrent_steps,
                                  local_index > 0))
          def _():
            plgpu.barrier_wait(consumed_barrier.at[slot])
          plgpu.copy_gmem_to_smem(
              a_gmem.at[slice_m, slice_k],
              a_smem.at[slot],
              a_tma_barrier.at[slot],
              leader_tracked=plgpu.CopyPartition.PARTITIONED(0)
              if collective
              else None,
              collective_axes=collective_axis,
          )
          plgpu.copy_gmem_to_smem(
              b_gmem.at[slice_k, slice_n],
              b_smem.at[slot],
              b_tma_barrier.at[slot],
              leader_tracked=plgpu.CopyPartition.PARTITIONED(1)
              if collective
              else None,
              collective_axes=collective_axis,
          )
        lax.fori_loop(0, k_iters, _loop_body, None)

      @pl.when(jnp.logical_and(warp_id == MMA_WARP, local_index > 1))
      def _wait_store():
        plgpu.barrier_wait(store_done_barrier.at[acc_slot])
      @pl.when(jnp.logical_and(warp_id == MMA_WARP, is_lead_block))
      def _compute():
        def _loop_body(ki, _):
          slot = lax.rem(ki, max_concurrent_steps)
          plgpu.barrier_wait(a_tma_barrier.at[slot])
          plgpu.barrier_wait(b_tma_barrier.at[slot])

          is_last_iter = ki >= k_iters - 1
          acc_tmem_slice = acc_tmem.at[:, pl.ds(acc_slot * tile_n, tile_n)]
          plgpu.tcgen05_mma(
              acc_tmem_slice,
              a_smem.at[slot],
              b_smem.at[slot],
              consumed_barrier.at[slot],
              accumulate=(ki > 0),
              collective_axis=collective_axis,
          )
          @pl.when(is_last_iter)
          def _():
            plgpu.tcgen05_commit_arrive(
                mma_done_barrier.at[acc_slot],
                collective_axis=collective_axis,
            )

        lax.fori_loop(0, k_iters, _loop_body, None)

  @pl.when(wg_idx == STORE_WG)
  @jax.named_scope("store_wg")
  def _():
    plgpu.barrier_wait(mma_done_barrier.at[acc_slot])
    acc_tmem_slot = acc_tmem.at[:, pl.ds(acc_slot * tile_n, tile_n)]
    step_out_gmem = out_gmem.at[block_slice_m, slice_n]
    # group_info contains start/size info relative to the logical
    # tiling (tile_m) but because for collective matmuls we use 2 CTAs per
    # logical block, but we need to compute the start/size relative to the
    # current block.
    # For example, for the following parameters:
    #     block_tile_m=64 (tile_m=128)
    #     group_info.start_within_block=60
    #     group_info.actual_size=37
    # The requested copy will be split across both blocks
    # Memory:         | Block 0  |  Block 1 |
    #                 |--- 64 ---|--- 64 ---|
    # Copy:                    |-- 37 --|
    # Where block 0 copies rows 60-64 (4 rows total) and block 1 copies
    # the remaining rows 64-97 (33 rows total).
    smem_start = group_info.start_within_block - cluster_idx * block_tile_m
    smem_start = lax.max(smem_start, jnp.int32(0))
    def _clamp(min, x, max):
      return lax.max(lax.min(x, max), min)
    block0_copy_size = _clamp(
        jnp.int32(0),
        block_tile_m - group_info.start_within_block,
        group_info.actual_size)
    block_local_size = lax.select(is_lead_block,
      # block 0 copies up to end of the first block or actual_size,
      # whichever comes first.
      block0_copy_size,
      # block 1 copies the remaining rows that block 0 did not copy.
      group_info.actual_size - block0_copy_size
    )
    for ni in range(tile_n // epilogue_tile_n):
      acc_smem[...] = plgpu.async_load_tmem(
          acc_tmem_slot.at[:, pl.ds(ni * epilogue_tile_n, epilogue_tile_n)],
          layout=regs_layout).astype(dtype)
      plgpu.commit_smem()
      cur_smem_idx = smem_start
      remaining_rows = min(block_tile_m, m)
      while remaining_rows > 0:
        const_rows_len = 1 << int(math.log2(remaining_rows))
        remaining_rows //= 2
        @pl.when(block_local_size & const_rows_len != 0)
        def _():
          o_smem_slice = acc_smem.at[pl.ds(cur_smem_idx, const_rows_len)]
          o_gref_slice = step_out_gmem.at[
              pl.ds(cur_smem_idx, const_rows_len),
              pl.ds(ni * epilogue_tile_n, epilogue_tile_n),
          ]
          plgpu.copy_smem_to_gmem(o_smem_slice, o_gref_slice)
        cur_smem_idx += block_local_size & const_rows_len
      plgpu.wait_smem_to_gmem(0, wait_read_only=True)
    plgpu.wait_load_tmem()  # Load must complete before we continue.
    plgpu.barrier_arrive(store_done_barrier.at[acc_slot])

