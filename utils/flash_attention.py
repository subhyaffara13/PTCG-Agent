
def flash_attention(
    q,  # [batch_size, num_heads, q_seq_len, d_model]
    k,  # [batch_size, num_heads, kv_seq_len, d_model]
    v,  # [batch_size, num_heads, kv_seq_len, d_model]
    ab=None,  # [batch_size, num_heads, q_seq_len, kv_seq_len]
    segment_ids=None,  # q of [batch_size, q_seq_len] and kv of [batch_size, kv_seq_len]
    *,
    causal: bool = False,
    sm_scale: float = 1.0,
    block_sizes: BlockSizes | None = None,
    debug: bool = False,
):
  batch_size, num_heads, q_seq_len, d_model = q.shape
  batch_size_k, num_heads_k, kv_seq_len, d_model_k = k.shape
  batch_size_v, num_heads_v, kv_seq_len_v, d_model_v = v.shape
  if batch_size != batch_size_k or batch_size != batch_size_v:
    raise ValueError(
        f"Batch size mismatch: got {batch_size}, {batch_size_k} and"
        f" {batch_size_v} (for q, k, v respectively)"
    )
  if num_heads != num_heads_k or num_heads != num_heads_v:
    raise ValueError(
        f"Head count mismatch: got {num_heads}, {num_heads_k},"
        f" {num_heads_v} (for q, k, v respectively)"
    )
  if d_model != d_model_k:
    raise ValueError(
        f"Model dimension mismatch: got {d_model} and {d_model_k} (for q and k"
        " respectively)"
    )
  if d_model != d_model_v:
    raise NotImplementedError(
        "V model dimension unequal to KV model dimension unsupported"
    )
  if kv_seq_len != kv_seq_len_v:
    raise ValueError(
        f"KV sequence length mismatch: got {kv_seq_len} and {kv_seq_len_v}"
    )
  if ab is not None:
    if ab.shape != (batch_size, num_heads, q_seq_len, kv_seq_len):
      raise ValueError(
          f"Attention bias shape mismatch: expected ({batch_size=},"
          f" {num_heads=}, {q_seq_len=}, {kv_seq_len=}), got {ab.shape}"
      )
  if segment_ids is not None:
    if segment_ids.q.shape != (batch_size, q_seq_len):
      raise ValueError(
          f"Q segment ids shape mismatch: expected ({batch_size=},"
          f" {q_seq_len=},), got {segment_ids.q.shape}"
      )
    if segment_ids.kv.shape != (batch_size, kv_seq_len):
      raise ValueError(
          f"KV segment ids shape mismatch: expected ({batch_size=},"
          f" {kv_seq_len=},), got {segment_ids.kv.shape}"
      )
  if block_sizes is None:
    block_sizes = BlockSizes.get_default(
        batch_size, num_heads, q_seq_len, kv_seq_len, d_model
    )
  return _flash_attention(
      q, k, v, ab, segment_ids, False, causal, sm_scale, block_sizes, debug
  )

