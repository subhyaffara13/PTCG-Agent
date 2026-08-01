
def ref_ragged_paged_attention(
    queries: jax.Array,  # [max_num_batched_tokens, num_q_heads, head_dim]
    kv_pages: jax.Array,  # [total_num_pages, page_size, num_combined_kv_heads, head_dim]
    kv_lens: jax.Array,  # i32[max_num_seqs]
    page_indices: jax.Array,  # i32[max_num_seqs, pages_per_seq]
    cu_q_lens: jax.Array,  # i32[max_num_seqs + 1]
    num_seqs: jax.Array,  # i32[1],
    *,
    sm_scale: float = 1.0,
    sliding_window: int | None = None,
    soft_cap: float | None = None,
    mask_value: float | None = DEFAULT_MASK_VALUE,
    k_scale: float | None = None,
    v_scale: float | None = None,
):
  static_validate_inputs(
      queries,
      kv_pages,
      kv_lens,
      page_indices,
      cu_q_lens,
      num_seqs,
      sm_scale=sm_scale,
      k_scale=k_scale,
      v_scale=v_scale,
      sliding_window=sliding_window,
      soft_cap=soft_cap,
      mask_value=mask_value,
  )
  if mask_value is None:
    mask_value = DEFAULT_MASK_VALUE
  _, _, num_combined_kv_heads, head_dim = kv_pages.shape
  assert num_combined_kv_heads % 2 == 0
  num_kv_heads = num_combined_kv_heads // 2
  num_q_heads = queries.shape[1]
  assert num_q_heads % num_kv_heads == 0
  num_query_per_kv = num_q_heads // num_kv_heads
  outputs = []
  for i in range(num_seqs[0]):
    q_start = cu_q_lens[i]
    q_end = cu_q_lens[i + 1]
    q_len = q_end - q_start
    kv_len = kv_lens[i]
    indices = page_indices[i]
    q = queries[q_start:q_end]
    k = kv_pages[indices, :, 0::2, :].reshape(-1, num_kv_heads, head_dim)[
        :kv_len
    ]
    v = kv_pages[indices, :, 1::2, :].reshape(-1, num_kv_heads, head_dim)[
        :kv_len
    ]
    if k_scale is not None:
      k = k.astype(jnp.float32) * k_scale
      k = k.astype(q.dtype)
    if v_scale is not None:
      v = v.astype(jnp.float32) * v_scale
      v = v.astype(q.dtype)
    k = jnp.repeat(k, num_query_per_kv, axis=1)
    v = jnp.repeat(v, num_query_per_kv, axis=1)
    attn = jnp.einsum("qhd,khd->hqk", q, k, preferred_element_type=jnp.float32)
    attn *= sm_scale
    q_span = (kv_len - q_len) + jax.lax.broadcasted_iota(
        jnp.int32, attn.shape, 1
    )
    kv_span = jax.lax.broadcasted_iota(jnp.int32, attn.shape, 2)
    mask = q_span < kv_span
    if sliding_window is not None:
      mask = jnp.logical_or(mask, q_span - sliding_window >= kv_span)
    if soft_cap is not None:
      attn = soft_cap * jnp.tanh(attn / soft_cap)
    attn += jnp.where(mask, mask_value, 0.0)
    attn = jax.nn.softmax(attn, axis=-1).astype(v.dtype)
    out = jnp.einsum("hqk,khd->qhd", attn, v).astype(queries.dtype)
    outputs.append(out)

  return jnp.concatenate(outputs, axis=0)

