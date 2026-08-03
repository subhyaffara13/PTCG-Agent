from typing import Any
import math


def mha_forward_kernel(
    q_ref,
    k_ref,
    v_ref,  # Input arrays
    segment_ids_ref: jax.Array | None,  # segment_id arrays
    o_ref: Any,  # Output
    *residual_refs: Any,  # Residual outputs
    sm_scale: float,
    causal: bool,
    block_q: int,
    block_k: int,
    head_dim: int,
):
  seq_len = k_ref.shape[0]
  start_q = pl.program_id(0)
  head_dim_padded = q_ref.shape[-1]

  # o is the buffer where we accumulate the output on sram.
  # m_i and l_i (see FlashAttention paper) are updated during the k,v loop.
  m_i = jnp.zeros(block_q, dtype=jnp.float32) - float('inf')
  l_i = jnp.zeros(block_q, dtype=jnp.float32)
  # acc is the buffer where we accumulate the output on sram.
  o = jnp.zeros((block_q, head_dim_padded), dtype=jnp.float32)

  # Load q: it will stay in L1 throughout. Indices form a matrix because we
  # read, compute, and write all in 2d chunks. 1 element ~= 1 CUDA thread index.
  # q tile has shape [block_q, head_dim_padded], head_dim_padded >= head_dim.
  curr_q_slice = pl.dslice(start_q * block_q, block_q)
  head_mask = (jnp.arange(head_dim_padded) < head_dim)[None, :]
  q = plgpu.load(q_ref, mask=head_mask, other=0.0)
  q_segment_ids = (
      None if segment_ids_ref is None else segment_ids_ref[curr_q_slice]
  )
  # In FlashAttention algorithm 1 there are 2 loops: slow over tiles of kv (size
  # (Bc == block_k here), and fast over blocks of q (size Br == block_q here).
  # Here we only loop over blocks of kv to process entire seq_len, the loop over
  # blocks of q is carried out by the grid.
  def body(start_k, carry):
    o_prev, m_prev, l_prev = carry
    curr_k_slice = pl.dslice(start_k * block_k, block_k)

    k = plgpu.load(k_ref.at[curr_k_slice, :], mask=head_mask, other=0.0)
    qk = plgpu.dot(q, k.T)   # [block_q, block_k]

    # Scale logits to convert from base-2 to the natural log domain.
    # This is based on the identity: e^x = 2^(x * log2(e)).
    qk_scale = math.log2(math.e)
    if sm_scale != 1.:
      qk_scale *= sm_scale
    qk *= qk_scale

    # Avoids Triton crash.
    # if num_heads > 2:
    #   qk = qk.astype(q_ref.dtype)
    #   qk = qk.astype(jnp.float32)

    if causal or segment_ids_ref is not None:
      mask = None
      if segment_ids_ref is not None:
        assert q_segment_ids is not None
        kv_segment_ids = segment_ids_ref[curr_k_slice]
        mask = segment_mask(q_segment_ids, kv_segment_ids)
      if causal:
        span_q = start_q * block_q + jnp.arange(block_q)
        span_k = start_k * block_k + jnp.arange(block_k)
        causal_mask = span_q[:, None] >= span_k[None, :]
        mask = (
            causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
        )
      # Apply mask to qk.
      assert mask is not None
      qk = jnp.where(mask, qk, DEFAULT_MASK_VALUE)

    m_curr = jnp.max(qk, axis=-1)
    m_next = jnp.maximum(m_prev, m_curr)
    correction = jnp.exp2(m_prev - m_next)
    l_prev_corr = correction * l_prev
    s_curr = jnp.exp2(
        qk - m_next[:, None]
    )  # Use m_next instead of m_curr to avoid a correction on l_curr
    l_curr = s_curr.sum(axis=-1)
    l_next = l_prev_corr + l_curr
    o_prev_corr = correction[:, None] * o_prev
    v = plgpu.load(v_ref.at[curr_k_slice, :], mask=head_mask)
    o_curr = plgpu.dot(s_curr.astype(v.dtype), v)

    o_next = o_prev_corr + o_curr
    return o_next, m_next, l_next
  if causal:
    # Ceildiv (`pl.cdiv` and `//` do not work due to type of start_q)
    upper_bound = lax.div(block_q * (start_q + 1) + block_k - 1, block_k)
  else:
    upper_bound = pl.cdiv(seq_len, block_k)
  o, m_i, l_i = lax.fori_loop(0, upper_bound, body, (o, m_i, l_i))

  # We keep an unscaled version of o during the scan over seq_len. Scaling it
  # by the last l_i gives us the correct final output. See section 3.1.1 in the
  # FlashAttention-2 paper: https://arxiv.org/pdf/2307.08691.
  o /= l_i[:, None]

  if residual_refs:
    lse_ref = residual_refs[0]
    lse_ref[...] = m_i + jnp.log2(l_i)
  # Write output to dram.
  plgpu.store(o_ref.at[:, : o.shape[-1]], o.astype(o_ref.dtype), mask=head_mask)

