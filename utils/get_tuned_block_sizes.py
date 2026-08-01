
def get_tuned_block_sizes(
    q_dtype,
    kv_dtype,
    num_q_heads_per_blk,
    num_kv_heads_per_blk,
    head_dim,
    page_size,
    max_num_batched_tokens,
    pages_per_seq,
) -> tuple[int, int]:
  """Look up for the best (num_kv_pages_per_blk, num_queries_per_blk) from auto-tuned table."""
  tpu_version = get_tpu_version()
  if tpu_version < 4:
    raise NotImplementedError('TPU version must be 4 or higher.')
  key = (
      q_dtype,
      kv_dtype,
      num_q_heads_per_blk,
      num_kv_heads_per_blk,
      head_dim,
      page_size,
      max_num_batched_tokens,
      pages_per_seq,
  )
  key = simplify_key(key)
  device_name = get_device_name()

  # Default block sizes.
  bkv, bq = (128, 32)
  if tpu_version == 4:
    # This default block size is not tuned, only make sure there's no
    # OOM in vmem
    bkv, bq = (32, 32)
  elif device_name in TUNED_BLOCK_SIZES:
    if key in TUNED_BLOCK_SIZES[device_name]:
      bkv, bq = TUNED_BLOCK_SIZES[device_name][key]
  return (min(pages_per_seq, bkv), min(max_num_batched_tokens, bq))

