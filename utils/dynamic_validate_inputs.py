
def dynamic_validate_inputs(
    q: jax.Array,  # [max_num_batched_tokens, num_q_heads, head_dim]
    kv_pages: jax.Array,  # [total_num_pages, page_size, num_combined_kv_heads, head_dim]
    kv_lens: jax.Array,  # i32[max_num_seqs]
    page_indices: jax.Array,  # i32[max_num_seqs, pages_per_seq]
    cu_q_lens: jax.Array,  # i32[max_num_seqs + 1]
    num_seqs: jax.Array,  # i32[1]
    *,
    # These inputs are optional. If not specified, we will not validate them.
    sm_scale: float | None = None,
    sliding_window: int | None = None,
    soft_cap: float | None = None,
    mask_value: float | None = None,
    k_scale: float | None = None,
    v_scale: float | None = None,
    # Kernel tuning params.
    num_kv_pages_per_block: int | None = None,
    num_queries_per_block: int | None = None,
    vmem_limit_bytes: int | None = None,
):
  static_validate_inputs(
      q,
      kv_pages,
      kv_lens,
      page_indices,
      cu_q_lens,
      num_seqs,
      sm_scale=sm_scale,
      sliding_window=sliding_window,
      soft_cap=soft_cap,
      mask_value=mask_value,
      k_scale=k_scale,
      v_scale=v_scale,
      num_kv_pages_per_block=num_kv_pages_per_block,
      num_queries_per_block=num_queries_per_block,
      vmem_limit_bytes=vmem_limit_bytes,
  )
  max_num_batched_tokens = q.shape[0]
  page_size = kv_pages.shape[1]
  max_num_seqs, pages_per_seq = page_indices.shape
  if num_seqs[0] > max_num_seqs:
    raise ValueError(f"{num_seqs[0]=} must be less or equal to {max_num_seqs=}")
  max_kv_len = jnp.max(kv_lens)
  min_pages_per_seq = pl.cdiv(max_kv_len, page_size)
  if pages_per_seq < min_pages_per_seq:
    raise ValueError(
        f"{pages_per_seq=} must be greater or equal to"
        f" {min_pages_per_seq=} given {max_kv_len=} and {page_size=}."
    )
  if cu_q_lens[num_seqs[0]] > max_num_batched_tokens:
    raise ValueError(
        f"Total q tokens {cu_q_lens[num_seqs[0]]} must be less or equal to"
        f" {max_num_batched_tokens=}."
    )
  for i in range(num_seqs[0]):
    q_len = cu_q_lens[i + 1] - cu_q_lens[i]
    kv_len = kv_lens[i]
    if q_len > kv_len:
      raise ValueError(
          f"{q_len=} must be less or equal to {kv_len=} at sequence {i}."
      )

