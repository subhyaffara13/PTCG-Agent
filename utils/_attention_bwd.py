
def _attention_bwd(config: TuningConfig, save_residuals: bool, res, do):
  del save_residuals
  q, k, v, out, lse = res

  if config.causal:
    raise NotImplementedError("Causal attention not supported in the backwards pass yet.")

  if not config.has_backward_blocks:
    raise ValueError("Need to specify backward blocks.")

  assert config.block_q_dq is not None
  assert config.block_kv_dq is not None
  assert config.block_q_dkv is not None
  assert config.block_kv_dkv is not None

  batch_size, q_seq_len, num_q_heads, head_dim = q.shape
  _, kv_seq_len, num_kv_heads, _ = k.shape
  q_heads_per_kv_head = num_q_heads // num_kv_heads
  dtype = q.dtype
  compute_wgs = config.compute_wgs_bwd

  num_q_tiles, rem = divmod(q_seq_len, config.block_q_dq * compute_wgs)
  if rem:
    raise NotImplementedError(
        f"{q_seq_len=} must be a multiple of {config.block_q_dq=} * {compute_wgs=}")

  num_kv_tiles, rem = divmod(kv_seq_len, config.block_kv_dkv * compute_wgs)
  if rem:
    raise NotImplementedError(
        f"{kv_seq_len=} must be a multiple of {config.block_kv_dkv=} * {compute_wgs=}")

  num_q_tiles_in_dkv, rem = divmod(q_seq_len, config.block_q_dkv)
  if rem:
    raise NotImplementedError(f"{q_seq_len=} must be a multiple of {config.block_q_dkv=}")

  num_kv_tiles_in_dq, rem = divmod(kv_seq_len, config.block_kv_dq)
  if rem:
    raise NotImplementedError(f"{kv_seq_len=} must be a multiple of {config.block_kv_dq=}")

  tiling = plgpu.TilingTransform((8, 64))
  swizzle = plgpu.SwizzleTransform(128)

  delta = jnp.einsum('bqhd,bqhd->bhq', out.astype(jnp.float32), do.astype(jnp.float32))
  del out  # Not needed anymore.

  def kernel_dq(q_ref, k_ref, v_ref, do_ref, lse_ref, delta_ref, dq_ref,
                smem_buffers, buffer_barriers, block_q, block_kv):
    batch = lax.axis_index("batch")
    q_head = lax.axis_index("heads")
    wg_idx = lax.axis_index("wg")
    kv_head = lax.div(q_head, jnp.array(q_heads_per_kv_head, q_head.dtype))
    q_smem2, do_smem2, lse_smem2, delta_smem2 = smem_buffers
    q_barriers, do_barriers, lse_barriers, delta_barriers = buffer_barriers
    def _compute_thread(pipeline_callback: PipelineCallback, /) -> None:
      q_smem, do_smem, lse_smem, delta_smem = q_smem2.at[wg_idx], do_smem2.at[wg_idx], lse_smem2.at[wg_idx], delta_smem2.at[wg_idx]
      q_seq_base = lax.axis_index("q_seq") * (compute_wgs * block_q) + wg_idx * block_q
      q_slice = (batch, pl.ds(q_seq_base, block_q), q_head)
      plgpu.copy_gmem_to_smem(q_ref.at[q_slice], q_smem, q_barriers.at[wg_idx])
      plgpu.copy_gmem_to_smem(do_ref.at[q_slice], do_smem, do_barriers.at[wg_idx])
      plgpu.copy_gmem_to_smem(
          delta_ref.at[batch, q_head, pl.ds(q_seq_base, block_q)],
          delta_smem,
          delta_barriers.at[wg_idx],
      )
      plgpu.copy_gmem_to_smem(
          lse_ref.at[batch, q_head, pl.ds(q_seq_base, block_q)],
          lse_smem,
          lse_barriers.at[wg_idx],
      )
      for buffer in buffer_barriers:
        plgpu.barrier_wait(buffer.at[wg_idx])

      delta = plgpu.load(delta_smem, (), layout=plgpu.Layout.WGMMA.reduce(1))
      lse = plgpu.load(lse_smem, (), layout=plgpu.Layout.WGMMA.reduce(1))
      dq_acc: jax.Array = plgpu.layout_cast(
          jnp.full((block_q, head_dim), 0, dtype=jnp.float32), plgpu.Layout.WGMMA,
      )
      dq, _, _ = pipeline_callback((dq_acc, lse, delta))
      q_smem[...] = dq.astype(dtype)
      plgpu.commit_smem()
      plgpu.copy_smem_to_gmem(q_smem, dq_ref.at[q_slice])
      plgpu.wait_smem_to_gmem(0)

    def kv_pipeline(_, k_smem, v_smem, k_consumed_barrier, v_consumed_barrier, carry):
      q_smem, do_smem = q_smem2.at[wg_idx], do_smem2.at[wg_idx]
      (dq_acc, lse, delta) = carry

      def compute_s(acc_ref):
        plgpu.wgmma(acc_ref, q_smem, plgpu.transpose_ref(k_smem, (1, 0)))
        return acc_ref[...]

      s = pl.run_scoped(compute_s, plgpu.ACC((block_q, block_kv), jnp.float32))
      s *= math.log2(math.e)
      p = jnp.exp2(s - lax.broadcast_in_dim(lse, (block_q, block_kv), [0]))

      # dP
      def compute_dp(acc_ref):
        plgpu.wgmma(acc_ref, do_smem, plgpu.transpose_ref(v_smem, (1, 0)))
        return acc_ref[...]

      dp = pl.run_scoped(compute_dp, plgpu.ACC((block_q, block_kv), jnp.float32))
      plgpu.barrier_arrive(v_consumed_barrier)

      # dS
      ds = p * (dp - lax.broadcast_in_dim(delta, (block_q, block_kv), [0]))

      # dQ
      def compute_dq(acc_ref):
        plgpu.wgmma(acc_ref, ds.astype(k_ref.dtype), k_smem)

      dq_acc = pl.run_state(compute_dq)(plgpu.ACC.init(dq_acc))
      plgpu.barrier_arrive(k_consumed_barrier)

      return (dq_acc, lse, delta)

    pipeline = plgpu.emit_pipeline_warp_specialized(
        kv_pipeline,
        grid=(num_kv_tiles_in_dq,),
        max_concurrent_steps=min([config.max_concurrent_steps, num_q_tiles]),
        num_compute_wgs=compute_wgs,
        memory_registers=40,
        wg_axis="wg",
        manual_consumed_barriers=True,
        compute_context=_compute_thread,
        in_specs=[
            plgpu.BlockSpec(  # k
                block_shape=(block_kv, head_dim),
                index_map=lambda i: (i, 0),
                transforms=[tiling, swizzle]),
            plgpu.BlockSpec(  # v
                block_shape=(block_kv, head_dim),
                index_map=lambda i: (i, 0),
                transforms=[tiling, swizzle]),
        ])
    k_ref = k_ref.at[batch, :, kv_head, :]
    v_ref = v_ref.at[batch, :, kv_head, :]
    pipeline(k_ref, v_ref)

  def kernel_dkv(q_ref, k_ref, v_ref, do_ref, lse_ref, delta_ref,
                 dk_ref, dv_ref, smem_buffers, buffer_barriers, block_q: int, block_kv: int):
    batch = lax.axis_index("batch")
    q_head = lax.axis_index("heads")
    wg_idx = lax.axis_index("wg")
    (k_smem2, v_smem2) = smem_buffers
    (k_barriers, v_barriers) = buffer_barriers

    def _compute_thread(pipeline_callback):
      k_smem, v_smem = k_smem2.at[wg_idx], v_smem2.at[wg_idx]
      kv_seq_base = lax.axis_index("kv_seq") * (compute_wgs * block_kv) + wg_idx * block_kv
      kv_head = lax.div(q_head, jnp.array(q_heads_per_kv_head, q_head.dtype))
      plgpu.copy_gmem_to_smem(
          k_ref.at[(batch, pl.ds(kv_seq_base, block_kv), kv_head)],
          k_smem,
          k_barriers.at[wg_idx])
      plgpu.copy_gmem_to_smem(
          v_ref.at[(batch, pl.ds(kv_seq_base, block_kv), kv_head)],
          v_smem,
          v_barriers.at[wg_idx])
      plgpu.barrier_wait(k_barriers.at[wg_idx])
      plgpu.barrier_wait(v_barriers.at[wg_idx])
      dk_acc = plgpu.layout_cast(
          jnp.full((block_kv, head_dim), 0, dtype=jnp.float32), plgpu.Layout.WGMMA,
      )
      dv_acc = plgpu.layout_cast(
          jnp.full((block_kv, head_dim), 0, dtype=jnp.float32), plgpu.Layout.WGMMA,
      )
      (dk, dv) = pipeline_callback((dv_acc, dk_acc))
      k_smem[...] = dk.astype(dtype)
      v_smem[...] = dv.astype(dtype)

      plgpu.commit_smem()
      plgpu.copy_smem_to_gmem(
          k_smem,
          dk_ref.at[(batch, pl.ds(kv_seq_base, block_kv), q_head)],
          commit_group=False)
      plgpu.copy_smem_to_gmem(
          v_smem,
          dv_ref.at[(batch, pl.ds(kv_seq_base, block_kv), q_head)],
          commit_group=False)
      plgpu.commit_smem_to_gmem_group()
      plgpu.wait_smem_to_gmem(0)

    def q_pipeline(_, q_smem, do_smem, lse_smem, delta_smem, q_consumed_barrier, do_consumed_barrier, lse_consumed_barrier, delta_consumed_barrier, carry):
      k_smem, v_smem = k_smem2.at[wg_idx], v_smem2.at[wg_idx]
      dk_acc, dv_acc = carry

      def _compute_sT(acc_ref):
        plgpu.wgmma(acc_ref, k_smem, plgpu.transpose_ref(q_smem, (1, 0)))
        return acc_ref[...]
      sT = pl.run_scoped(_compute_sT, plgpu.ACC((block_kv, block_q), jnp.float32))
      sT *= math.log2(math.e)

      lse = plgpu.load(lse_smem, (), layout=plgpu.Layout.WGMMA.reduce(0))
      plgpu.barrier_arrive(lse_consumed_barrier)
      pT = jnp.exp2(sT - lax.broadcast_in_dim(lse, (block_kv, block_q), [1]))

      def _compute(refs):
        # Combining two WGMMA calls in one block to avoid the unnecessary
        # synchronization from two `wgmma.wait_group` calls.
        dv_acc_ref, dpT_acc_ref = refs
        plgpu.wgmma(dv_acc_ref, pT.astype(dtype), do_smem)  # dV
        plgpu.wgmma(dpT_acc_ref, v_smem, plgpu.transpose_ref(do_smem, (1, 0)))  # dpT

      zeros = plgpu.layout_cast(
          jnp.full((block_kv, block_q), 0, dtype=jnp.float32), plgpu.Layout.WGMMA,
      )
      dv_acc, dpT = pl.run_state(_compute)((plgpu.ACC.init(dv_acc), plgpu.ACC.init(zeros)))
      plgpu.barrier_arrive(do_consumed_barrier)

      delta = plgpu.load(delta_smem, (), layout=plgpu.Layout.WGMMA.reduce(0))
      plgpu.barrier_arrive(delta_consumed_barrier)

      dsT = pT * (dpT - lax.broadcast_in_dim(delta, (block_kv, block_q), [1]))  # jax-operator-types

      def compute_dk(acc_ref):
        plgpu.wgmma(acc_ref, dsT.astype(dtype), q_smem)

      dk_acc = pl.run_state(compute_dk)(plgpu.ACC.init(dk_acc))
      plgpu.barrier_arrive(q_consumed_barrier)

      return (dk_acc, dv_acc)

    pipeline = plgpu.emit_pipeline_warp_specialized(
      q_pipeline,
      grid=(num_q_tiles_in_dkv,),
      max_concurrent_steps=min([config.max_concurrent_steps, num_kv_tiles]),
      num_compute_wgs=compute_wgs,
      memory_registers=40,
      wg_axis="wg",
      manual_consumed_barriers=True,
      compute_context=_compute_thread,
      in_specs=[
          plgpu.BlockSpec(  # q
              block_shape=(block_q, head_dim),
              index_map=lambda i: (i, 0),
              transforms=[tiling, swizzle]),
          plgpu.BlockSpec(  # do
              block_shape=(block_q, head_dim),
              index_map=lambda i: (i, 0),
              transforms=[tiling, swizzle]),
          plgpu.BlockSpec(block_shape=(block_q,), index_map=lambda i: (i,)),
          plgpu.BlockSpec(block_shape=(block_q,), index_map=lambda i: (i,))
      ])
    q_ref = q_ref.at[batch, :, q_head, :]
    do_ref = do_ref.at[batch, :, q_head, :]
    lse_ref = lse_ref.at[batch, q_head, :]
    delta_ref = delta_ref.at[batch, q_head, :]
    pipeline(q_ref, do_ref, lse_ref, delta_ref)

  q_scratch = plgpu.SMEM(
      (compute_wgs, config.block_q_dq, head_dim), jnp.float16,
      transforms=(tiling, swizzle),
  )
  do_scratch = q_scratch
  lse_scratch = plgpu.SMEM((compute_wgs, config.block_q_dq), jnp.float32)
  delta_scratch = plgpu.SMEM((compute_wgs, config.block_q_dq), jnp.float32)
  dq = plgpu.kernel(
      partial(kernel_dq, block_q=config.block_q_dq, block_kv=config.block_kv_dq),
      out_type=q,
      scratch_types=[
          (q_scratch, do_scratch, lse_scratch, delta_scratch),
          (plgpu.Barrier(num_barriers=compute_wgs),) * 4
      ],
      compiler_params=plgpu.CompilerParams(approx_math=True),
      grid=(num_q_heads, num_q_tiles, batch_size),
      grid_names=("heads", "q_seq", "batch"),
      num_threads=compute_wgs + 1,
      thread_name="wg",
  )(q, k, v, do, lse, delta)

  k_scratch = plgpu.SMEM(
          (compute_wgs, config.block_kv_dkv, head_dim), jnp.float16,
          transforms=(tiling, swizzle),
      )
  v_scratch = k_scratch
  out_shape_kv = jax.ShapeDtypeStruct(
      (batch_size, kv_seq_len, num_q_heads, head_dim), dtype=jnp.float16)
  dk, dv = plgpu.kernel(
    partial(kernel_dkv, block_q=config.block_q_dkv, block_kv=config.block_kv_dkv),
    out_type=[out_shape_kv, out_shape_kv],
    scratch_types=[
        (k_scratch, v_scratch),
        (plgpu.Barrier(num_barriers=compute_wgs),) * 2
  ],
    compiler_params=plgpu.CompilerParams(approx_math=True),
    grid=(num_q_heads, num_kv_tiles, batch_size),
    grid_names=("heads", "kv_seq", "batch"),
    num_threads=compute_wgs + 1,
    thread_name="wg"
  )(q, k, v, do, lse, delta)

  if q_heads_per_kv_head > 1:
    sum_shape = (*k.shape[:-1], q_heads_per_kv_head, head_dim)
    dk = dk.reshape(sum_shape).astype(jnp.float32).sum(axis=-2).astype(dk.dtype)
    dv = dv.reshape(sum_shape).astype(jnp.float32).sum(axis=-2).astype(dv.dtype)

  return dq, dk, dv

