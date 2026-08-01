
def decode_attn_unbatched(
    q,           # [num_heads, head_dim]
    k,           # [k_seq_len, head_dim]
    v,           # [k_seq_len, head_dim]
    start_idx,   # []
    kv_seq_len,  # []
    sm_scale: float,
    block_h: int,
    block_k: int,
    k_splits: int,
    num_warps: int | None,
    num_stages: int,
    grid: tuple[int, ...] | None,
    interpret: bool,
    debug: bool,
    return_residuals: bool,
    normalize_output: bool
):
  num_heads, head_dim = q.shape
  k_seq_len, _ = k.shape
  # Pad num query heads to 16 if needed, and slice output at the end.
  head_splits = pl.cdiv(num_heads, block_h)
  grid_ = grid
  if grid_ is None:
    grid_ = (head_splits, k_splits)

  assert (
      k_seq_len % k_splits == 0
  ), f"{k_seq_len=} must be divisible by {k_splits=}"
  assert k_seq_len // k_splits >= 16, (
    f"{k_seq_len=} divided by {k_splits=} must be >= 16.")
  assert block_k >= 16, "block_k must be >= 16"
  k = k.reshape(k_splits, k_seq_len // k_splits, head_dim)
  v = v.reshape(k_splits, k_seq_len // k_splits, head_dim)
  split_k_seq_len = k_seq_len // k_splits
  block_k = min(block_k, split_k_seq_len)
  assert split_k_seq_len % block_k == 0, (
    f"Sequence length ({k_seq_len=}) split by {k_splits=} must by divisible by"
    f" {block_k=}")
  num_warps_ = num_warps
  if num_warps_ is None:
    num_warps_ = 4
  kernel = functools.partial(
      attn_forward_kernel,
      sm_scale=sm_scale,
      block_k=block_k,
      block_h=block_h,
      num_heads=num_heads,
  )

  o, l, m = pl.pallas_call(
    kernel,
    grid=grid_,
    in_specs=[
      pl.BlockSpec((block_h, head_dim), lambda i, j: (i, 0)),
      pl.BlockSpec((None, split_k_seq_len, head_dim), lambda i, j: (j, 0, 0)),
      pl.BlockSpec((None, split_k_seq_len, head_dim), lambda i, j: (j, 0, 0)),
    ]
    + [None if start_idx is None else pl.BlockSpec((), lambda i, j: ())]
    + [None if kv_seq_len is None else pl.BlockSpec((), lambda i, j: ())],
    out_specs=[
      pl.BlockSpec((None, block_h, head_dim), lambda i, j: (j, i, 0)),  # o
      pl.BlockSpec((None, block_h), lambda i, j: (j, i)),  # l
      pl.BlockSpec((None, block_h), lambda i, j: (j, i)),  # m
    ],
    compiler_params=plgpu.CompilerParams(
      num_warps=num_warps_, num_stages=num_stages
    ),
    out_shape=[
      jax.ShapeDtypeStruct(shape=(k_splits, *q.shape), dtype=q.dtype),  # o
      jax.ShapeDtypeStruct(
        shape=(k_splits, num_heads), dtype=jnp.float32
      ),  # l
      jax.ShapeDtypeStruct(
        shape=(k_splits, num_heads), dtype=jnp.float32
      ),  # m
    ],
    debug=debug,
    interpret=interpret,
    name="mha_forward",
  )(q, k, v, start_idx, kv_seq_len)

  # final round of flash
  m_next = m.max(axis=0)
  # TODO(b/389925439): This barrier is necessary to prevent NaNs/invalid
  # values appearing after JIT compilation.
  m_next = lax.optimization_barrier(m_next)
  correction = jnp.exp(m - m_next[None])
  o = o * correction[:, :, None].astype(o.dtype)
  l_next = (l * correction).sum(axis=0)
  eps = jnp.finfo(l_next.dtype).eps
  o = o.sum(axis=0)
  if normalize_output:
    o /= (l_next[:, None].astype(o.dtype) + eps)
  if return_residuals:
    return o, (l_next, m_next)
  else:
    return o

