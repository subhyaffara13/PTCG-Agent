
def static_validate_inputs(
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
  _, num_q_heads, head_dim = q.shape
  _, _, num_combined_kv_heads, head_dim_k = kv_pages.shape
  assert num_combined_kv_heads % 2 == 0
  assert isinstance(k_scale, float) or k_scale is None
  assert isinstance(v_scale, float) or v_scale is None
  num_kv_heads = num_combined_kv_heads // 2
  max_num_seqs, pages_per_seq = page_indices.shape
  if num_seqs.shape != (1,):
    raise ValueError(f"{num_seqs.shape=} must be (1,)")
  if head_dim_k != head_dim:
    raise ValueError(
        f"Q head_dim {head_dim} must be the same as that of K/V {head_dim_k}."
    )
  if kv_lens.shape != (max_num_seqs,):
    raise ValueError(
        f"Expected {kv_lens.shape=} to be ({max_num_seqs},) where"
        " `max_num_seqs` is `page_indices.shape[0]`."
    )
  if cu_q_lens.shape != (max_num_seqs + 1,):
    raise ValueError(
        f"Expected {cu_q_lens.shape=} to be ({max_num_seqs + 1},)  where"
        " `max_num_seqs` is `page_indices.shape[0]`."
    )
  if (
      kv_lens.dtype != jnp.int32
      or page_indices.dtype != jnp.int32
      or cu_q_lens.dtype != jnp.int32
  ):
    raise ValueError(
        "The dtype of `kv_lens`, `page_indices`, and `cu_q_lens` must be"
        f" int32. Got {kv_lens.dtype=}, {page_indices.dtype=},"
        f" {cu_q_lens.dtype=}."
    )
  if num_q_heads % num_kv_heads != 0:
    raise ValueError(f"{num_q_heads=} must be divisible by {num_kv_heads=}")
  if sliding_window is not None and sliding_window <= 0:
    raise ValueError(f"{sliding_window=} must be positive.")
  if soft_cap is not None and soft_cap == 0.0:
    raise ValueError(f"{soft_cap=} must not be 0.0.")
  if (
      num_kv_pages_per_block is not None
      and not 0 < num_kv_pages_per_block <= pages_per_seq
  ):
    raise ValueError(
        f"{num_kv_pages_per_block=} must be in range (0, {pages_per_seq}]."
    )
  if num_queries_per_block is not None and num_queries_per_block <= 0:
    raise ValueError(f"{num_queries_per_block=} must be positive.")
  if vmem_limit_bytes is not None and vmem_limit_bytes <= 0:
    raise ValueError(f"{vmem_limit_bytes=} must be positive.")
  del sm_scale  # No constraints on sm_scale.
  del mask_value  # No consstraints on mask_value.

