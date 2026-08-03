from typing import Any

def _flash_attention_kernel_single_batch_single_step(
    batch_idx: tuple[int, ...],
    q_tile_ref,
    k_tile_ref,
    v_tile_ref,
    ab_tile_ref,
    q_segment_ids_tile_ref,
    kv_segment_ids_tile_ref,  # Input arrays
    o_tile_ref,  # Output arrays
    l_ref: Any | None = None,
    m_ref: Any | None = None,
    *,
    causal,
    sm_scale,
    block_k,
    kv_seq_len,
    mask_value,
):
  block_k_major = k_tile_ref.shape[2]
  block_q = q_tile_ref.shape[2]

  assert kv_seq_len == block_k_major == block_k

  q = q_tile_ref[batch_idx]  # [block_q, head_dim]
  k = k_tile_ref[batch_idx]  # [block_k, head_dim]
  s = jax.lax.dot_general(
      q, k, TRANS_B_DIM_NUMBERS, preferred_element_type=jnp.float32
  )  # [block_q, block_k]

  if ab_tile_ref is not None:
    s += ab_tile_ref[batch_idx].astype(jnp.float32)
  if sm_scale != 1.0:
    s *= sm_scale

  mask = None
  if q_segment_ids_tile_ref is not None:
    repeats, rem = divmod(block_k, NUM_LANES)
    if rem:
      raise NotImplementedError(
          f"kv block size must be a multiple of {NUM_LANES}"
      )
    q_segment_ids = q_segment_ids_tile_ref[
        batch_idx[0]
    ]  # [block_q, NUM_LANES].
    q_segment_ids = jnp.tile(
        q_segment_ids, (1, repeats)
    )  # [block_q, block_k].
    kv_segment_ids = kv_segment_ids_tile_ref[batch_idx[0], :1]  # [1, block_k].
    mask = jnp.equal(q_segment_ids, kv_segment_ids).astype(jnp.bool_)

  if causal:
    q_seq_idx = pl.program_id(2)
    mask_shape = (block_q, block_k)
    row_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 0)
    row_ids += q_seq_idx * block_q
    col_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 1)
    causal_mask = col_ids <= row_ids
    mask = causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
  s = s if mask is None else s + jnp.where(mask, 0.0, mask_value)

  m = jnp.max(s, axis=1)[:, None]
  p = jnp.exp(s - m)
  l = jnp.sum(p, axis=1)[:, None]
  p /= l

  if m_ref is not None:
    m_ref[batch_idx] = lax.broadcast_in_dim(m, m_ref.shape[2:], range(2))
  if l_ref is not None:
    l_ref[batch_idx] = lax.broadcast_in_dim(l, l_ref.shape[2:], range(2))

  v = v_tile_ref[batch_idx]
  o_tile_ref[batch_idx] = jax.lax.dot(
      p.astype(v.dtype), v, preferred_element_type=jnp.float32
  ).astype(o_tile_ref.dtype)

