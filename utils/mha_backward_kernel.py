import math


def mha_backward_kernel(
    # Inputs
    q_ref,
    k_ref,
    v_ref,
    segment_ids_ref: jax.Array | None,
    out_ref,
    do_scaled_ref,
    lse_ref,
    delta_ref,
    # Outputs
    dq_ref,
    dk_ref,
    dv_ref,
    *,
    sm_scale: float,
    causal: bool,
    block_q_dkv: int,
    block_kv_dkv: int,
    block_q_dq: int,
    block_kv_dq: int,
    head_dim: int,
):
  del out_ref  # Not needed
  q_seq_len = q_ref.shape[0]
  kv_seq_len = k_ref.shape[0]

  # Scan #1: dK and dV
  #   1. Load a block of K and V of size (block_kv_dkv, head_dim) in SMEM.
  #   2. Iterate through Q in chunks of (block_q_dkv, head_dim) to accumulate
  #      dK and dV.
  start_k = pl.program_id(2)
  curr_k_slice = pl.dslice(start_k * block_kv_dkv, block_kv_dkv)

  head_dim_padded = q_ref.shape[-1]
  dv = jnp.zeros([block_kv_dkv, head_dim_padded], dtype=jnp.float32)
  dk = jnp.zeros([block_kv_dkv, head_dim_padded], dtype=jnp.float32)

  head_mask = (jnp.arange(head_dim_padded) < head_dim)[None, :]
  v = plgpu.load(v_ref.at[curr_k_slice, :], mask=head_mask, other=0.0)
  k = plgpu.load(k_ref.at[curr_k_slice, :], mask=head_mask, other=0.0)
  span_k = start_k * block_kv_dkv + jnp.arange(block_kv_dkv)
  kv_segment_ids = (
      None if segment_ids_ref is None else segment_ids_ref[curr_k_slice]
  )

  def inner_loop_dkdv(start_q, carry):
    dv, dk = carry
    curr_q_slice = pl.dslice(start_q * block_q_dkv, block_q_dkv)

    q = plgpu.load(q_ref.at[curr_q_slice, :], mask=head_mask, other=0.0)
    qk = plgpu.dot(q, k.T)
    qk_scale = math.log2(math.e)
    if sm_scale != 1.:
      qk_scale *= sm_scale
    qk *= qk_scale

    if causal or segment_ids_ref is not None:
      mask = None
      if segment_ids_ref is not None:
        assert kv_segment_ids is not None
        q_segment_ids = segment_ids_ref[curr_q_slice]
        mask = segment_mask(q_segment_ids, kv_segment_ids)

      if causal:
        span_q = start_q * block_q_dkv + jnp.arange(block_q_dkv)
        causal_mask = span_q[:, None] >= span_k[None, :]
        mask = (
            causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
        )
      assert mask is not None
      qk = jnp.where(mask, qk, DEFAULT_MASK_VALUE)

    lse = lse_ref[curr_q_slice]
    di = delta_ref[curr_q_slice]
    do = plgpu.load(
        do_scaled_ref.at[curr_q_slice, :], mask=head_mask, other=0.0
    )

    p = jnp.exp2(qk - lse[:, None])
    dv = dv + plgpu.dot(p.astype(do.dtype).T, do)
    dp = jnp.zeros((block_q_dkv, block_kv_dkv), dtype=jnp.float32) - di[:, None]
    dp = dp + plgpu.dot(do, v.T)
    ds = p * dp
    if sm_scale != 1.0:
      ds = ds * sm_scale
    dk = dk + plgpu.dot(ds.astype(q_ref.dtype).T, q)

    return dv, dk

  lower_bound = lax.div(start_k * block_kv_dkv, block_q_dkv) if causal else 0
  dv, dk = lax.fori_loop(
      lower_bound, pl.cdiv(q_seq_len, block_q_dkv), inner_loop_dkdv, (dv, dk)
  )
  plgpu.store(
      dv_ref.at[:, : dv.shape[-1]], dv.astype(dv_ref.dtype), mask=head_mask
  )
  plgpu.store(
      dk_ref.at[:, : dk.shape[-1]], dk.astype(dk_ref.dtype), mask=head_mask
  )

  # Scan #2: dQ
  #   1. Load a block of Q of size (block_q_dq, head_dim) in SMEM.
  #   2. Iterate through K and V in chunks of (block_kv_dq, head_dim) to
  #     accumulate dQ.
  start_q = pl.program_id(2)
  curr_q_slice = pl.ds(start_q * block_q_dq, block_q_dq)
  span_q = start_q * block_q_dq + jnp.arange(block_q_dq)
  dq = jnp.zeros([block_q_dq, head_dim_padded], dtype=jnp.float32)

  q = plgpu.load(q_ref.at[curr_q_slice, :], mask=head_mask, other=0.0)
  q_segment_ids = (
      None if segment_ids_ref is None else segment_ids_ref[curr_q_slice]
  )
  lse = lse_ref[curr_q_slice]
  do = plgpu.load(do_scaled_ref.at[curr_q_slice, :], mask=head_mask, other=0.0)
  di = delta_ref[curr_q_slice]

  def inner_loop_dq(start_k, dq):
    curr_k_slice = pl.dslice(start_k * block_kv_dq, block_kv_dq)
    k = plgpu.load(k_ref.at[curr_k_slice, :], mask=head_mask, other=0.0)
    v = plgpu.load(v_ref.at[curr_k_slice, :], mask=head_mask, other=0.0)

    qk = plgpu.dot(q, k.T)
    qk_scale = math.log2(math.e)
    if sm_scale != 1.:
      qk_scale *= sm_scale
    qk *= qk_scale

    if causal or segment_ids_ref is not None:
      mask = None
      if segment_ids_ref is not None:
        assert q_segment_ids is not None
        kv_segment_ids = segment_ids_ref[curr_k_slice]
        mask = segment_mask(q_segment_ids, kv_segment_ids)

      if causal:
        span_k = start_k * block_kv_dq + jnp.arange(block_kv_dq)
        causal_mask = span_q[:, None] >= span_k[None, :]
        mask = (
            causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
        )
      assert mask is not None
      qk = jnp.where(mask, qk, DEFAULT_MASK_VALUE)

    p = jnp.exp2(qk - lse[:, None])
    dp = jnp.zeros((block_q_dq, block_kv_dq), dtype=jnp.float32) - di[:, None]
    dp = dp + plgpu.dot(do, v.T)
    ds = p * dp
    if sm_scale != 1.0:
      ds = ds * sm_scale

    dq = dq + plgpu.dot(ds.astype(k.dtype), k).astype(dq.dtype)

    return dq

  if causal:
    upper_bound = pl.cdiv((start_q + 1) * block_q_dq, block_kv_dq)
  else:
    upper_bound = pl.cdiv(kv_seq_len, block_kv_dq)

  dq = lax.fori_loop(0, upper_bound, inner_loop_dq, (dq))
  plgpu.store(
      dq_ref.at[:, : dq.shape[-1]], dq.astype(dq_ref.dtype), mask=head_mask
  )

