import functools

def mixed_matmul_kernel(
    a: jax.Array, b: jax.Array, *, out_dtype: jnp.dtype, config: TuningConfig
) -> jax.Array:
  """Mixed-type matrix multiplication kernel for Hopper GPUs.

  Specifically, this kernel implements the function
    (a.as_dtype(b.dtype) @ b).astype(out_dtype).
  """
  if a.dtype == b.dtype:
    raise ValueError(
        f"Mixed matmul LHS and RHS have the same dtype {a.dtype}. For such "
        "matrix multiplications, use the `hopper_matmul_mgpu` kernel instead."
    )
  match (a.dtype, b.dtype):
    case (jnp.int8, jnp.bfloat16):
      pass
    case (jnp.int8, jnp.float16):
      pass
    case _, _:
      # We do support more combinations, but we haven't benchmarked them
      # yet---so we raise for the time being.
      raise NotImplementedError(
          f"Unbenchmarked dtype combination: {a.dtype=} and {b.dtype=}"
      )
  m, k = a.shape
  k2, n = b.shape
  if k != k2:
    raise ValueError(
        f"Matmul LHS and RHS have incompatible shapes {a.shape} vs {b.shape}"
    )

  tile_m, tile_n, tile_k = config.tile_m, config.tile_n, config.tile_k
  epi_tile_n = config.epi_tile_n or tile_n
  epi_tile_m = config.epi_tile_m or tile_m
  if tile_n % epi_tile_n != 0:
    raise ValueError(f"{tile_n=} must be divisible by {epi_tile_n=}")
  if tile_m % epi_tile_m != 0:
    raise ValueError(f"{tile_m=} must be divisible by {epi_tile_m=}")

  a_bits = dtypes.itemsize_bits(a.dtype)
  b_bits = dtypes.itemsize_bits(b.dtype)
  out_bits = dtypes.itemsize_bits(out_dtype)

  a_swizzle = plgpu.find_swizzle(tile_k * a_bits, "lhs")
  b_swizzle = plgpu.find_swizzle(tile_n * b_bits, "rhs")
  out_swizzle = plgpu.find_swizzle(epi_tile_n * out_bits, "out")

  a_transforms = (
      plgpu.TilingTransform((8, a_swizzle * 8 // a_bits)),
      plgpu.SwizzleTransform(a_swizzle),
  )
  b_transforms = (
      plgpu.TilingTransform((8, b_swizzle * 8 // b_bits)),
      plgpu.SwizzleTransform(b_swizzle),
  )
  out_transforms = (
      plgpu.TilingTransform((8, out_swizzle * 8 // out_bits)),
      plgpu.SwizzleTransform(out_swizzle),
  )

  max_concurrent_steps = config.max_concurrent_steps
  cta_tile_m = tile_m * (1 + (config.wg_dimension == MatmulDimension.M))
  cta_tile_n = tile_n * (1 + (config.wg_dimension == MatmulDimension.N))
  cluster_tile_m = cta_tile_m * (1 + (config.cluster_dimension == MatmulDimension.M))
  cluster_tile_n = cta_tile_n * (1 + (config.cluster_dimension == MatmulDimension.N))
  if m % cluster_tile_m != 0:
    raise ValueError(f"{m=} must be divisible by {cluster_tile_m} for the given config")
  if n % cluster_tile_n != 0:
    raise ValueError(f"{n=} must be divisible by {cluster_tile_n} for the given config")
  if k % tile_k != 0:
    raise ValueError(f"{k=} must be divisible by {tile_k=}")
  m_iters = m // cluster_tile_m
  n_iters = n // cluster_tile_n
  k_iters = k // tile_k

  def kernel(a_gmem, b_gmem, out_gmem, out_smem):

    def get_pipeline(pipeline_body, compute_context):
      return plgpu.emit_pipeline_warp_specialized(
          pipeline_body,
          grid=(k_iters,),
          memory_registers=40,
          in_specs=[
              plgpu.BlockSpec(
                  (cta_tile_m, tile_k),
                  lambda k: (0, k),
                  transforms=a_transforms,
                  memory_space=plgpu.SMEM,
                  collective_axes=("cluster",)
                  if config.cluster_dimension == MatmulDimension.N
                  else (),
              ),
              plgpu.BlockSpec(
                  (tile_k, cta_tile_n),
                  lambda k: (k, 0),
                  transforms=b_transforms,
                  memory_space=plgpu.SMEM,
                  collective_axes=("cluster",)
                  if config.cluster_dimension == MatmulDimension.M
                  else (),
              ),
          ],
          wg_axis="wg",
          num_compute_wgs=2,
          max_concurrent_steps=max_concurrent_steps,
          compute_context=compute_context,
      )

    # Functions don't influence the allocations necessary to run the pipeline.
    ignore = lambda *_, **__: None
    @functools.partial(
        pl.run_scoped,
        pipeline_allocs=get_pipeline(ignore, ignore).get_allocations(a_gmem, b_gmem),
        collective_axes="wg",
    )
    def _pipeline_scope(pipeline_allocs):
      wg_idx = lax.axis_index("wg")
      cta_idx = lax.axis_index("cluster")
      @plgpu.nd_loop((m_iters * n_iters,), collective_axes="cluster_grid")
      def _mn_loop(loop_info: plgpu.NDLoopInfo):
        (lin_idx,) = loop_info.index
        m_cluster_idx, n_cluster_idx = plgpu.planar_snake(
            lin_idx,
            (m_iters, n_iters),
            config.grid_minor_dim,
            config.grid_tile_width,
        )
        m_idx = m_cluster_idx
        n_idx = n_cluster_idx
        if config.cluster_dimension == MatmulDimension.M:
          m_idx = m_cluster_idx * 2 + cta_idx
        elif config.cluster_dimension == MatmulDimension.N:
          n_idx = n_cluster_idx * 2 + cta_idx
        cta_m_slice = pl.ds(m_idx * cta_tile_m, cta_tile_m)
        cta_n_slice = pl.ds(n_idx * cta_tile_n, cta_tile_n)
        if config.wg_dimension == MatmulDimension.M:
          wg_m_slice = pl.ds(wg_idx * tile_m, tile_m)
          wg_n_slice = slice(None)
        else:
          wg_m_slice = slice(None)
          wg_n_slice = pl.ds(wg_idx * tile_n, tile_n)

        def compute_context(eval_pipeline):
          @functools.partial(
              pl.run_scoped, acc_ref=plgpu.ACC((tile_m, tile_n), jnp.float32)
          )
          def _acc_scope(acc_ref):
            eval_pipeline(acc_ref)
            acc = acc_ref[...].astype(out_dtype)
            plgpu.wait_smem_to_gmem(0, wait_read_only=True)
            for epi_mi in range(tile_m // epi_tile_m):
              for epi_ni in range(tile_n // epi_tile_n):
                epi_m_slice = slice(epi_mi * epi_tile_m, (epi_mi + 1) * epi_tile_m)
                epi_n_slice = slice(epi_ni * epi_tile_n, (epi_ni + 1) * epi_tile_n)
                slot = (epi_mi * (tile_n // epi_tile_n) + epi_ni) % 2
                plgpu.wait_smem_to_gmem(1, wait_read_only=True)
                out_smem[wg_idx, slot] = acc[epi_m_slice, epi_n_slice]
                plgpu.commit_smem()
                plgpu.copy_smem_to_gmem(
                    out_smem.at[wg_idx, slot],
                    out_gmem.at[cta_m_slice, cta_n_slice]
                    .at[wg_m_slice, wg_n_slice]
                    .at[epi_m_slice, epi_n_slice],
                )

        def mma_body(_, a_smem, b_smem, acc_ref):
          with jax.named_scope("smem_load"):
            a_reg = a_smem[wg_m_slice]
          with jax.named_scope("dequant"):
            a_reg = a_reg.astype(b.dtype)
          with jax.named_scope("wgmma"):
            plgpu.wgmma(acc_ref, a_reg, b_smem.at[:, wg_n_slice])
          with jax.named_scope("wgmma_wait"):
            plgpu.wgmma_wait(0)
          return acc_ref

        get_pipeline(mma_body, compute_context)(
            a_gmem.at[cta_m_slice, :],
            b_gmem.at[:, cta_n_slice],
            allocations=pipeline_allocs,
        )
    # Await all transfers before we exit.
    plgpu.wait_smem_to_gmem(0, wait_read_only=True)

  # We don't need multiple slots if there's only one epilogue tile.
  num_out_slots = min(2, (tile_m * tile_n) // (epi_tile_m * epi_tile_n))
  num_sms = backend.get_default_device().core_count
  cluster_size = 1 + (config.cluster_dimension is not None)
  compiler_params = plgpu.CompilerParams(
      lowering_semantics=plgpu.LoweringSemantics.Warpgroup
  )
  f = plgpu.kernel(
      kernel,
      out_type=jax.ShapeDtypeStruct((m, n), out_dtype),
      grid=(num_sms // cluster_size,),
      grid_names=("cluster_grid",),
      cluster=(cluster_size,),
      cluster_names=("cluster",),
      num_threads=3,
      thread_name="wg",
      compiler_params=compiler_params,
      scratch_types=dict(
          out_smem=plgpu.SMEM(
              (2, num_out_slots, epi_tile_m, epi_tile_n),
              out_dtype,
              transforms=out_transforms,
          )
      ),
  )
  return f(a, b)

