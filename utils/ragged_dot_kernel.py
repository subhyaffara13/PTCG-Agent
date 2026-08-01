
def ragged_dot_kernel(a, b, group_sizes, config: TuningConfig):
  dtype = a.dtype
  if a.dtype != b.dtype:
    raise ValueError(
        f"Matmul LHS and RHS have incompatible dtypes {a.dtype} vs {b.dtype}"
    )
  m, k = a.shape
  num_groups, k2, n = b.shape
  if num_groups != group_sizes.shape[0]:
    raise ValueError("RHS and group_sizes have incompatible shapes.")
  if k != k2:
    raise ValueError(
        "Matmul LHS and RHS have incompatible shapes "
        f"{a.shape} vs {b.shape[1:]}"
    )
  collective = config.collective
  tile_m, tile_n, tile_k = (config.tile_m, config.tile_n, config.tile_k)
  block_tile_m = tile_m
  block_tile_n = tile_n
  if collective:
    tile_m *= 2
    tile_n *= 2
  m_iters = m // tile_m
  n_iters = n // tile_n

  max_concurrent_steps = config.max_concurrent_steps
  epilogue_tile_n = config.epilogue_tile_n
  if tile_n % epilogue_tile_n != 0:
    raise ValueError(
        f"{tile_n=} must be divisible by {epilogue_tile_n=}"
    )

  if m % tile_m != 0:
    raise ValueError(f"{m=} must be divisible by {tile_m=}")
  if n % tile_n != 0:
    raise ValueError(f"{n=} must be divisible by {tile_n=}")
  if k % tile_k != 0:
    raise ValueError(f"{k=} must be divisible by {tile_k=}")
  swizzle = plgpu.find_swizzle(tile_k * jnp.dtype(dtype).itemsize * 8)
  swizzle_elems = swizzle // jnp.dtype(dtype).itemsize
  transforms = (
      plgpu.TilingTransform((8, swizzle_elems)),
      plgpu.SwizzleTransform(swizzle),
  )

  def kernel(a_gmem, b_gmem, group_sizes_gmem, out_gmem):
    linear_grid = (m_iters + num_groups - 1) * n_iters
    group_sizes_regs = [group_sizes_gmem[i] for i in range(num_groups)]
    cluster_idx = lax.axis_index("x")

    @functools.partial(pl.run_scoped,
        a_smem=plgpu.SMEM(
            (max_concurrent_steps, block_tile_m, tile_k),
            dtype, transforms=transforms
        ),
        b_smem=plgpu.SMEM(
            (max_concurrent_steps, tile_k, block_tile_n),
            dtype, transforms=transforms
        ),
        # Temporary SMEM used for storing accumulator output to GMEM.
        acc_smem=plgpu.SMEM(
            (block_tile_m, epilogue_tile_n), dtype),
        # a/b_tma_barrier
        a_tma_barrier=plgpu.Barrier(num_arrivals=1, num_barriers=max_concurrent_steps),
        b_tma_barrier=plgpu.Barrier(num_arrivals=1, num_barriers=max_concurrent_steps),
        # store_done_barrier, double-buffered
        store_done_barrier=plgpu.Barrier(num_arrivals=1, num_barriers=2,
                      orders_tensor_core=True),
        # mma_done_barrier, double-buffered
        mma_done_barrier=plgpu.Barrier(num_arrivals=1, num_barriers=2,
                      orders_tensor_core=True),
        # consumed_barrier
        consumed_barrier=plgpu.Barrier(
            num_arrivals=1,
            num_barriers=max_concurrent_steps,
            orders_tensor_core=True,
        ),
        # Accumulator TMEM (double-buffered)
        acc_tmem=plgpu.TMEM(
            (block_tile_m, tile_n * 2), jnp.float32, collective=collective),
        collective_axes=("wg",)
    )
    def _scoped(**ref_kwargs):
      @plgpu.nd_loop(grid=(linear_grid,),
                     collective_axes="sm")
      def mn_loop(loop_info: plgpu.NDLoopInfo):
        linear_idx, = loop_info.index
        local_index = loop_info.local_index
        m_index, n_index = plgpu.planar_snake(
          linear_idx,
          (m_iters + num_groups - 1, n_iters),
          config.grid_minor_dim,
          config.grid_tile_width,
        )
        with jax.named_scope("create_group_info"):
          group_info = ragged_dot_mgpu.GroupInfo.create(
              group_sizes_regs, tile_m, m_index
          )
        do_matmul(
            a_gmem,
            b_gmem.at[group_info.group_id],
            out_gmem,
            grid_indices=(group_info.block, n_index, cluster_idx),
            wg_axis="wg",
            collective_axes=("x",) if collective else (),
            local_index=local_index,
            config=config,
            group_info=group_info,
            **ref_kwargs
        )

  num_sms = jax.local_devices()[0].core_count
  compiler_params = plgpu.CompilerParams(
      lowering_semantics=plgpu.LoweringSemantics.Warpgroup
  )
  f = plgpu.kernel(
      kernel,
      compiler_params=compiler_params,
      kernel_name=f"ragged_dot_kernel_{str(config)}",
      out_type=jax.ShapeDtypeStruct((m, n), dtype),
      grid=(num_sms//2,) if collective else (num_sms,),
      grid_names=("sm",),
      num_threads=2,
      thread_name="wg",
      cluster_names=("x",) if collective else (),
      cluster=(2,) if collective else (),
  )
  return f(a, b, group_sizes)

