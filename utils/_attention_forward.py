import functools
import math


def _attention_forward(q, k, v, config: TuningConfig, save_residuals: bool = False):
  assert cuda_versions is not None
  cuda_runtime_version = cuda_versions.cuda_runtime_get_version()
  # TODO(pobudzey): Undo when we upgrade to cuda 12.9.1.
  if config.causal and cuda_runtime_version >= 12080 and cuda_runtime_version < 12091:
    raise ValueError(
        "Causal masking not supported with cuda versions between 12.8.0 and"
        " 12.9.1 due to a ptxas miscompilation."
    )
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
  block_q, block_kv = config.block_q, config.block_kv
  if kv_seq_len % block_kv:
    raise ValueError(f"{kv_seq_len=} must be a multiple of {block_kv=}")

  def kernel(q_ref, k_ref, v_ref, out_ref, lse_ref, scoped):
    batch = lax.axis_index("batch")
    q_head = lax.axis_index("heads")
    smem_buffers, buffer_barriers, consumed_barriers, schedule_barrier = scoped
    wg_idx = lax.axis_index("wg")
    qo_smem2, k_smem, v_smem, lse_smem2 = smem_buffers
    k_barriers, v_barriers, q_barriers = buffer_barriers
    k_consumed_barriers, v_consumed_barriers = consumed_barriers
    def perform_schedule_barrier():
      plgpu.barrier_arrive(schedule_barrier)
      plgpu.barrier_wait(schedule_barrier)

    if config.causal:
      block_q_end = (lax.axis_index("q_seq") + 1) * (2 * block_q)
      block_max_kv_steps = pl.cdiv(block_q_end, jnp.array(block_kv, jnp.int32))
    else:
      block_max_kv_steps = kv_seq_len // block_kv

    @pl.when(wg_idx < 2)
    def _compute_wg():
      plgpu.set_max_registers(232, action="increase")
      qo_smem = qo_smem2.at[wg_idx]
      lse_smem = lse_smem2.at[wg_idx] if lse_smem2 is not None else None
      q_seq_base = lax.axis_index("q_seq") * (2 * block_q) + wg_idx * block_q

      if config.causal:
        kv_steps = pl.cdiv(q_seq_base + block_q, jnp.array(block_kv, jnp.int32))
      else:
        kv_steps = block_max_kv_steps

      plgpu.copy_gmem_to_smem(
          q_ref.at[batch, pl.ds(q_seq_base, block_q), q_head],
          qo_smem,
          q_barriers.at[wg_idx],
      )
      plgpu.barrier_wait(q_barriers.at[wg_idx])

      m_i = plgpu.layout_cast(
          jnp.full((block_q,), -jnp.inf, dtype=jnp.float32),
          plgpu.Layout.WGMMA.reduce(1),
      )
      l_i = plgpu.layout_cast(
          jnp.full((block_q,), 0, dtype=jnp.float32),
          plgpu.Layout.WGMMA.reduce(1),
      )
      acc = plgpu.layout_cast(
          jnp.full((block_q, head_dim), 0, dtype=jnp.float32),
          plgpu.Layout.WGMMA,
      )

      @pl.when(kv_steps > 0)
      def _():
        plgpu.barrier_wait(k_barriers.at[0])

      pl.when(wg_idx == 1)(perform_schedule_barrier)
      def kv_loop(kv_step, carry, causal: bool = False):
        acc, m_i, l_i = carry
        slot = lax.rem(kv_step, jnp.array(max_concurrent_steps, kv_step.dtype))

        # QK
        def compute_qk(acc_ref):
          plgpu.wgmma(acc_ref, qo_smem, plgpu.transpose_ref(k_smem.at[slot], (1, 0)))
          perform_schedule_barrier()
          return acc_ref[...]
        qk = pl.run_scoped(compute_qk, plgpu.ACC((block_q, block_kv), jnp.float32))
        plgpu.barrier_arrive(k_consumed_barriers.at[slot])

        if causal:
          q_ids = plgpu.broadcasted_iota(jnp.int32, (block_q, block_kv), 0, layout=plgpu.Layout.WGMMA)
          kv_ids = plgpu.broadcasted_iota(jnp.int32, (block_q, block_kv), 1, layout=plgpu.Layout.WGMMA)
          mask = (q_ids + q_seq_base) >= (kv_ids + kv_step * block_kv)
          qk = jnp.where(mask, qk, -jnp.inf)

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

        def end_softmax_barriers():
          plgpu.barrier_arrive(schedule_barrier)  # Done with softmax!
          plgpu.barrier_wait(v_barriers.at[slot])
          plgpu.barrier_wait(schedule_barrier)  # Wait until TensorCore is free.
        # Can't fully explain why, but empirically the ordering here influences
        # the performance of the final kernel quite significantly.
        if head_dim <= 128:
          l_i += p.sum(axis=1)
          acc, l_i, m_i, p16 = lax.optimization_barrier((acc, l_i, m_i, p16))
          end_softmax_barriers()
        else:
          end_softmax_barriers()
          l_i += p.sum(axis=1)

        # PV
        def compute_pv(acc_ref):
          plgpu.wgmma(acc_ref, p16, v_smem.at[slot])

          wait_step = kv_step + 1
          wait_slot = lax.rem(wait_step, jnp.array(max_concurrent_steps, kv_step.dtype))
          @pl.when(wait_step < kv_steps)
          def _wait():
            plgpu.barrier_wait(k_barriers.at[wait_slot])
        acc = pl.run_state(compute_pv)(plgpu.ACC.init(acc))
        plgpu.barrier_arrive(v_consumed_barriers.at[slot])
        return acc, m_i, l_i

      if not config.causal:
        acc, m_i, l_i = lax.fori_loop(0, block_max_kv_steps, kv_loop, (acc, m_i, l_i))
      else:
        def epilogue_kv_loop(kv_step, _):
          # This loop makes sure that all the pipelined KV data is processed, even
          # if one compute wg finishes early like with causal masking.
          slot = lax.rem(kv_step, jnp.array(max_concurrent_steps, kv_step.dtype))
          plgpu.barrier_arrive(k_consumed_barriers.at[slot])
          plgpu.barrier_arrive(v_consumed_barriers.at[slot])
          perform_schedule_barrier()
          perform_schedule_barrier()

        causal_kv_loop = functools.partial(kv_loop, causal=True)
        full_kv_steps = lax.div(q_seq_base, jnp.array(block_kv, jnp.int32))
        # With causal masking, the KV loop unrolling is split in 3 sections:
        # 1. A fast path where no causal mask is needed.
        acc, m_i, l_i = lax.fori_loop(0, full_kv_steps, kv_loop, (acc, m_i, l_i))
        # 2. Causal masking.
        acc, m_i, l_i = lax.fori_loop(full_kv_steps, kv_steps, causal_kv_loop, (acc, m_i, l_i))
        # 3. Epilogue to flush the data pipeline.
        lax.fori_loop(kv_steps, block_max_kv_steps, epilogue_kv_loop, None)
      pl.when(wg_idx == 0)(perform_schedule_barrier)

      # TODO(apaszke): Invert and multiply to avoid expensive divisions.
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
    @pl.when(wg_idx == 2)
    def _memory_wg():
      plgpu.set_max_registers(40, action="decrease")
      kv_head = lax.div(q_head, jnp.array(q_heads_per_kv_head, q_head.dtype))
      for i in range(max_concurrent_steps):
        s = (batch, pl.ds(i * block_kv, block_kv), kv_head)
        plgpu.copy_gmem_to_smem(k_ref.at[s], k_smem.at[i], k_barriers.at[i])
        plgpu.copy_gmem_to_smem(v_ref.at[s], v_smem.at[i], v_barriers.at[i])

      @pl.loop(0, block_max_kv_steps - max_concurrent_steps)
      def _kv_loop(kv_step):
        tma_step = kv_step + max_concurrent_steps
        tma_slot = lax.rem(kv_step, jnp.array(max_concurrent_steps, kv_step.dtype))
        s = (batch, pl.ds(tma_step * block_kv, block_kv), kv_head)
        plgpu.barrier_wait(k_consumed_barriers.at[tma_slot])
        plgpu.copy_gmem_to_smem(k_ref.at[s], k_smem.at[tma_slot], k_barriers.at[tma_slot])
        plgpu.barrier_wait(v_consumed_barriers.at[tma_slot])
        plgpu.copy_gmem_to_smem(v_ref.at[s], v_smem.at[tma_slot], v_barriers.at[tma_slot])

  def entry(q_ref, k_ref, v_ref, out_ref, lse_ref):
    compute_wgs = 2
    tiling = plgpu.TilingTransform((8, 64))
    swizzle = plgpu.SwizzleTransform(128)
    qo_scratch = plgpu.SMEM(
        (compute_wgs, block_q, head_dim), jnp.float16,
        transforms=(tiling, swizzle),
    )
    k_scratch = plgpu.SMEM(
        (max_concurrent_steps, block_kv, head_dim), jnp.float16,
        transforms=(tiling, swizzle),
    )
    v_scratch = plgpu.SMEM(
        (max_concurrent_steps, block_kv, head_dim), jnp.float16,
        transforms=(tiling, swizzle),
    )
    scratch = [qo_scratch, k_scratch, v_scratch, None]
    if save_residuals:
      scratch[3] = plgpu.SMEM((compute_wgs, block_q), jnp.float32)
    pl.run_scoped(
        lambda *args: kernel(q_ref, k_ref, v_ref, out_ref, lse_ref, args),
        scratch,
        (
            plgpu.Barrier(num_barriers=max_concurrent_steps),
            plgpu.Barrier(num_barriers=max_concurrent_steps),
            plgpu.Barrier(num_barriers=compute_wgs),
        ),
        (plgpu.Barrier(num_arrivals=compute_wgs, num_barriers=max_concurrent_steps),) * 2,
        plgpu.Barrier(num_arrivals=compute_wgs),
        collective_axes="wg",
    )

  num_q_tiles, rem = divmod(q_seq_len, block_q * 2)
  if rem:
    raise NotImplementedError(f"{q_seq_len=} must be a multiple of {block_q * 2=}")

  out_shape = [q, None]
  if save_residuals:
    # Note that we keep seq_len in the minor-most dimension so that we can do
    # 1D TMAs on chunks of `block_q`.
    out_shape[1] = jax.ShapeDtypeStruct(
        (batch_size, num_q_heads, q_seq_len), jnp.float32
    )

  out, lse = plgpu.kernel(
      entry,
      out_type=out_shape,
      grid=(num_q_heads, num_q_tiles, batch_size),
      grid_names=("heads", "q_seq", "batch"),
      num_threads=3,
      thread_name="wg",
      compiler_params=plgpu.CompilerParams(approx_math=True),
  )(q, k, v)

  if save_residuals:
    assert lse is not None
    return out, (lse,)

  return out

