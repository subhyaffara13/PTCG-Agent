
def check_layout(layout: torch.layout):
    torch._check_not_implemented(
        layout == torch.strided, lambda: f"PrimTorch doesn't support layout={layout}"
    )


def check_layout(query, key, value, bias, q_seqlen, kv_seqlen,
  q_offsets, kv_offsets, page_table_k, page_table_v, layout):
  def check_eq(a, b, c, msg):
    if not (a == b == c):
      raise ValueError(f"{msg} must be same, got {a}, {b}, {b}")

  q_rank, k_rank, v_rank = len(query.shape), len(key.shape), len(value.shape)
  if q_rank != 4:
    raise ValueError(f"Q must have a rank of 4, got {q_rank}")
  check_eq(q_rank, k_rank, v_rank, "QKV rank")

  q_dtype, k_dtype, v_dtype = query.dtype, key.dtype, value.dtype
  if q_dtype not in [np.float16, dtypes.bfloat16, dtypes.float8_e4m3fn, dtypes.float8_e5m2]:
    raise NotImplementedError(f"Q must be fp16/bf16/fp8_e4m3fn/fp8_e5m2, got {q_dtype}")
  check_eq(q_dtype, k_dtype, v_dtype, "QKV dtype")

  if layout == AttentionLayout.BNTH:
    qB, qN, qT, qH = query.shape
    kB, kN, kS, kH = key.shape
    vB, vN, vS, vH = value.shape
  else:
    assert layout == AttentionLayout.BTNH
    qB, qT, qN, qH = query.shape
    kB, kS, kN, kH = key.shape
    vB, vS, vN, vH = value.shape

  if page_table_k is not None and page_table_v is not None:
    k_blocks, k_block_size = kB, kS
    v_blocks, v_block_size = vB, vS
    kB, _, k_blocks_per_batch, _ = page_table_k.shape
    vB, _, v_blocks_per_batch, _ = page_table_v.shape
    kS = k_blocks_per_batch * k_block_size
    vS = v_blocks_per_batch * v_block_size
    if kB * k_blocks_per_batch != k_blocks:
      raise ValueError(
        f"Key and page_table_k must have same number of blocks, "
        f"got {k_blocks} vs {kB * k_blocks_per_batch}")
    if vB * v_blocks_per_batch != v_blocks:
      raise ValueError(
        f"Value and page_table_v must have same number of blocks, "
        f"got {v_blocks} vs {vB * v_blocks_per_batch}")

  check_eq(qB, kB, vB, "QKV batch")
  if qH != kH:
    raise ValueError(f"QK must have same head dim, got {qH} vs {kH}")
  if kN != vN:
    raise ValueError(f"KV must have same number of heads, got {kN} vs {vN}")
  if kS != vS:
    raise ValueError(f"KV must have same seq length, got {kS} vs {vS}")

  # check bias
  if bias is not None:
    _, _, bT, bS = bias.shape
    if bT != qT or bS != vS:
      raise ValueError(
        f"Bias must have same seq length as QKV, got {bT} and {bS}")

  # check q_seqlen/kv_seqlen/q_offsets/kv_offsets
  expected_rank = 2 if q_offsets is not None else 1
  def check_seqlen_offsets(tensor, name):
    if tensor is not None:
      dtype = tensor.dtype
      rank = len(tensor.shape)
      if dtype != np.dtype('int32'):
        raise ValueError(f"{name} must have int32 datatype, got {dtype}")
      if rank != expected_rank:
        raise ValueError(f"{name} must have a rank of {expected_rank}, got {rank}")
      b = tensor.shape[0]
      if b != qB:
        raise ValueError(f"{name} must have same batch as Q, got {b}")

  check_seqlen_offsets(q_seqlen, "q_seqlen")
  check_seqlen_offsets(kv_seqlen, "kv_seqlen")
  check_seqlen_offsets(q_offsets, "q_offsets")
  check_seqlen_offsets(kv_offsets, "kv_offsets")

