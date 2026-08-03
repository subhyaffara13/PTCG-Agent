from typing import Any

def attn_forward_kernel(
    # inputs
    q_ref,           # [num_heads, head_dim]
    k_ref,           # [k_seq_len, head_dim]
    v_ref,           # [k_seq_len, head_dim]
    start_idx_ref,   # [] (i.e., scalar)
    kv_seq_len_ref,  # [] (i.e., scalar)
    # outputs
    o_ref: Any,      # [num_heads, head_dim]
    *residual_refs: Any,  # Residual outputs: [num_heads,], [num_heads,]
    sm_scale: float,
    block_k: int,
    block_h: int,
    num_heads: int,
):
  _, head_dim = q_ref.shape
  split_k_seq_len, _ = k_ref.shape
  prog_i, prog_j = pl.program_id(0), pl.program_id(1)
  q_slice = pl.ds(0, block_h)
  q_mask = (jnp.arange(block_h) < num_heads - block_h * prog_i)[:, None]

  def _compute(start_idx, kv_seq_len, o, m_i, l_i):
    # Load q: it will stay in L1 throughout. Indices form a matrix because we
    # read, compute, and write all in 2d chunks. 1 element ~= 1 CUDA thread index.
    # q tile has shape [block_h, head_dim].
    q = plgpu.load(q_ref.at[q_slice, :], mask=q_mask)

    def _dot(a, b):
      # if a.shape[0] == 1:
      #   # Use matrix vector product
      #   return (a.T * b).sum(axis=0, keepdims=True)
      return plgpu.dot(a, b)

    mask_indices = jnp.arange(block_k)

    # Loop over blocks of kv to process entire kv seq_len.
    # Grid loops over q blocks over num_heads.
    def body(start_k, carry):
      o_prev, m_prev, l_prev = carry
      curr_k_slice = pl.ds(start_k * block_k, block_k)

      k = k_ref[curr_k_slice, :]
      qk = _dot(q, k.T)  # [block_h, block_k]
      if sm_scale != 1.0:
        qk *= sm_scale  # [block_h, block_k]

      # apply mask if start or sequence length is specified
      if start_idx_ref is not None or kv_seq_len_ref is not None:
        indices = (prog_j * split_k_seq_len + start_k * block_k + mask_indices)
        mask = ((indices >= start_idx) & (indices < kv_seq_len))[None, :]
        qk += (~mask) * (0.7 * jnp.finfo(qk.dtype).min)

      m_curr = qk.max(axis=-1)
      m_next = jnp.maximum(m_prev, m_curr)
      correction = jnp.exp(m_prev - m_next)
      l_prev_corr = correction * l_prev
      s_curr = jnp.exp(
          qk - m_next[:, None]
      )  # Use m_next instead of m_curr to avoid a correction on l_curr
      l_curr = s_curr.sum(axis=-1)
      l_next = l_prev_corr + l_curr
      v = v_ref[curr_k_slice, :]
      o_curr = _dot(s_curr.astype(v.dtype), v)

      # flash2 unscaled_o
      o_next = correction[:, None] * o_prev + o_curr
      return o_next, m_next, l_next

    max_it = jnp.minimum(pl.cdiv((kv_seq_len - prog_j * split_k_seq_len),
                                 block_k), split_k_seq_len // block_k)
    (o, m_i, l_i) = lax.fori_loop(0, max_it, body, (o, m_i, l_i))
    return o, m_i, l_i

  # o is the buffer where we accumulate the output on sram.
  # m_i and l_i (see FlashAttention2 paper) are updated during the k,v loop.
  m_i = jnp.zeros(block_h, dtype=jnp.float32) + jnp.finfo(jnp.float32).min
  l_i = jnp.zeros(block_h, dtype=jnp.float32)
  o = jnp.zeros((block_h, head_dim), dtype=jnp.float32)

  start_idx = split_k_seq_len * prog_j
  if start_idx_ref is not None:
    start_idx = jnp.maximum(start_idx, start_idx_ref[()])
  kv_seq_len = (prog_j + 1) * split_k_seq_len  # lower bound on actual k_seq_len
  if kv_seq_len_ref is not None:
    kv_seq_len = jnp.minimum(kv_seq_len, kv_seq_len_ref[()])

  if start_idx_ref is None and kv_seq_len is None:
    o, m_i, l_i = _compute(start_idx, kv_seq_len, o, m_i, l_i)
  else:
    o, m_i, l_i = jax.lax.cond(
      start_idx >= kv_seq_len, lambda: (o, m_i, l_i),
      lambda: _compute(start_idx, kv_seq_len, o, m_i, l_i))

  # Write output to dram.
  if residual_refs:
    l_ref, m_ref = residual_refs
    vec_q_mask = q_mask.reshape(-1) if q_mask is not None else None
    plgpu.store(l_ref.at[q_slice], l_i, mask=vec_q_mask)
    plgpu.store(m_ref.at[q_slice], m_i, mask=vec_q_mask)
  o = o.astype(o_ref.dtype)
  plgpu.store(o_ref.at[q_slice, :], o, mask=q_mask)

