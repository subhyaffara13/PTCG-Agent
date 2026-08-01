
def attention_with_pipeline_emitter(q, k, v, config: TuningConfig, save_residuals=False):
  if config.causal:
    raise NotImplementedError("Causal attention is not supported with the pipeline emitter yet.")
  if q.ndim != 4 or k.ndim != 4 or v.ndim != 4:
    raise ValueError(f"q, k, and v should all be 4D, got: {q.ndim=}, {k.ndim=}, {v.ndim=}")
  batch_size, q_seq_len, num_q_heads, head_dim = q.shape
  _, kv_seq_len, num_kv_heads, _ = k.shape
  kv_shape = (batch_size, kv_seq_len, num_kv_heads, head_dim)
  if k.shape != kv_shape:
    raise ValueError(f"Expected {k.shape=} to be {kv_shape} (inferred from q)")
  if k.shape != kv_shape:
    raise ValueError(f"Expected {v.shape=} to be {kv_shape} (inferred from q)")
  if (dtype := q.dtype) != k.dtype or dtype != v.dtype:
    raise ValueError(f"q, k, and v should all have the same dtype, got: {q.dtype}, {k.dtype}, {v.dtype}")
  if num_q_heads % num_kv_heads:
    raise ValueError(f"{num_q_heads=} must be divisible by and {num_kv_heads=}")
  q_heads_per_kv_head = num_q_heads // num_kv_heads
  if head_dim % 64:
    raise ValueError(f"{head_dim=} must be divisible by 64")
  if jnp.dtype(dtype) not in map(jnp.dtype, [jnp.float16, jnp.bfloat16]):
    raise NotImplementedError(f"Only f16 and bf16 are supported, got dtype: {dtype}")

  max_concurrent_steps = min(
      config.max_concurrent_steps, kv_seq_len // config.block_kv
  )
  compute_wgs = 2
  block_q, block_kv = config.block_q, config.block_kv
  num_q_tiles, rem = divmod(q_seq_len, block_q * 2)
  if rem:
    raise NotImplementedError(f"{q_seq_len=} must be a multiple of {block_q * 2=}")

  def fa3_kernel(q_ref, k_ref, v_ref, out_ref, lse_ref, smem_buffers, q_barriers, schedule_barrier):
    batch = lax.axis_index("batch")
    wg_idx = lax.axis_index("wg")
    qo_smem2, lse_smem2 = smem_buffers
    q_seq_base = lax.axis_index("q_seq") * (2 * block_q) + wg_idx * block_q
    q_head = lax.axis_index("heads")
    kv_head = lax.div(q_head, jnp.array(q_heads_per_kv_head, q_head.dtype))

    def perform_schedule_barrier():
      if config.use_schedule_barrier:
        plgpu.barrier_arrive(schedule_barrier)
        plgpu.barrier_wait(schedule_barrier)

    def _compute_thread(pipeline_callback: PipelineCallback, /) -> None:
      qo_smem = qo_smem2.at[wg_idx]
      lse_smem = lse_smem2.at[wg_idx] if lse_smem2 is not None else None
      m_i = jnp.full((block_q,), -jnp.inf, dtype=jnp.float32)
      l_i = jnp.full((block_q,), 0, dtype=jnp.float32)
      acc = jnp.full((block_q, head_dim), 0, dtype=jnp.float32)
      # Q is not pipelined, so we load in with a manual DMA.
      plgpu.copy_gmem_to_smem(
          q_ref.at[batch, pl.ds(q_seq_base, block_q), q_head],
          qo_smem,
          q_barriers.at[wg_idx],
      )
      plgpu.barrier_wait(q_barriers.at[wg_idx])
      pl.when(wg_idx == 1)(perform_schedule_barrier)
      final_carry = pipeline_callback((acc, m_i, l_i))
      pl.when(wg_idx == 0)(perform_schedule_barrier)
      acc, m_i, l_i = final_carry
      acc /= lax.broadcast_in_dim(l_i, (block_q, head_dim), [0])
      qo_smem[...] = acc.astype(dtype)
      if lse_smem is not None:
        RCP_LN2 = 1.4426950408889634
        log2 = lambda x: jnp.log(x) * RCP_LN2
        lse_smem[...] = m_i + log2(l_i)
      plgpu.commit_smem()
      plgpu.copy_smem_to_gmem(
          qo_smem, out_ref.at[batch, pl.ds(q_seq_base, block_q), q_head],
      )
      if lse_smem is not None:
        plgpu.copy_smem_to_gmem(
            lse_smem,
            lse_ref.at[batch, q_head, pl.ds(q_seq_base, block_q)],
        )
      plgpu.wait_smem_to_gmem(0)

    def kv_pipeline(_, k_smem, v_smem,
                    k_consumed_barrier, v_consumed_barrier,
                    carry):
      acc, m_i, l_i = carry
      qo_smem = qo_smem2.at[wg_idx]
      def compute_qk(acc_ref):
        plgpu.wgmma(acc_ref, qo_smem, plgpu.transpose_ref(k_smem, (1, 0)))
        perform_schedule_barrier()
        return acc_ref[...]
      qk = pl.run_scoped(compute_qk, plgpu.ACC((block_q, block_kv), jnp.float32))
      plgpu.barrier_arrive(k_consumed_barrier)

      # Softmax
      # We keep m scaled by log2e to use FMA instructions when computing p.
      log2e = math.log2(math.e)
      m_ij = jnp.maximum(m_i, qk.max(axis=1) * log2e)
      alpha = jnp.exp2(m_i - m_ij)
      m_i = m_ij
      p = jnp.exp2(qk * log2e - lax.broadcast_in_dim(m_ij, qk.shape, [0]))
      acc *= lax.broadcast_in_dim(alpha, acc.shape, [0])
      l_i *= alpha
      p16 = p.astype(dtype)
      perform_schedule_barrier()
      l_i += p.sum(axis=1)
      # PV
      def compute_pv(acc_ref):
        plgpu.wgmma(acc_ref, p16, v_smem)
      acc = pl.run_state(compute_pv)(plgpu.ACC.init(acc))
      plgpu.barrier_arrive(v_consumed_barrier)
      return acc, m_i, l_i
    pipeline = plgpu.emit_pipeline_warp_specialized(
        kv_pipeline,
        grid=(kv_seq_len // block_kv,),
        max_concurrent_steps=max_concurrent_steps,
        num_compute_wgs=compute_wgs,
        memory_registers=40,
        wg_axis="wg",
        manual_consumed_barriers=True,
        compute_context=_compute_thread,
        in_specs=[
            plgpu.BlockSpec(  # k
                block_shape=(block_kv, head_dim),
                index_map=lambda i: (i, 0)),
            plgpu.BlockSpec(  # v
                block_shape=(block_kv, head_dim),
                index_map=lambda i: (i, 0)),
        ],
        out_specs=[],
    )
    k_ref = k_ref.at[batch, :, kv_head, :]
    v_ref = v_ref.at[batch, :, kv_head, :]
    pipeline(k_ref, v_ref)

  out_shape = [q, None]
  if save_residuals:
    out_shape[1] = jax.ShapeDtypeStruct((batch_size, num_q_heads, q_seq_len), jnp.float32)

  qo_scratch = plgpu.SMEM((compute_wgs, block_q, head_dim), jnp.float16)
  smem_scratch = [qo_scratch, None]
  if save_residuals:
    smem_scratch[1] = plgpu.SMEM((compute_wgs, block_q), jnp.float32)

  out, lse = plgpu.kernel(
      fa3_kernel,
      grid=(num_q_heads, num_q_tiles, batch_size),
      grid_names=("heads", "q_seq", "batch"),
      num_threads=3,
      thread_name="wg",
      out_type=out_shape,
      scratch_types=(
          tuple(smem_scratch),
          plgpu.Barrier(num_barriers=compute_wgs),
          plgpu.Barrier(num_arrivals=compute_wgs),),
      compiler_params=plgpu.CompilerParams(
          approx_math=True, lowering_semantics=plgpu.LoweringSemantics.Warpgroup,
      ),
  )(q, k, v)

  if save_residuals:
    assert lse is not None
    return out, (lse,)

  return out

