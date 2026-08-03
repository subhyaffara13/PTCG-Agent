import functools

def mha(
    q,
    k,
    v,
    segment_ids: jnp.ndarray | None,
    sm_scale: float = 1.0,
    causal: bool = False,
    block_sizes: BlockSizes = BlockSizes.get_default(),
    backward_pass_impl: str = "triton",
    num_warps: int | None = None,
    num_stages: int = 2,
    grid: tuple[int, ...] | None = None,
    interpret: bool = False,
    debug: bool = False,
    return_residuals: bool = False,
):
  del backward_pass_impl
  batch_size, q_seq_len, num_heads, head_dim = q.shape
  kv_seq_len = k.shape[1]
  block_q = min(block_sizes.block_q, q_seq_len)
  block_k = min(block_sizes.block_k, kv_seq_len)
  head_dim_padded = pl.next_power_of_2(head_dim)
  if (q.shape[-1] != k.shape[-1]) or (q.shape[-1] != v.shape[-1]):
    raise ValueError(
        f"This kernel expects q, k, and v to have the same head dimension, but"
        f" found {q.shape=}, {k.shape=}, {v.shape=}."
    )
  if q_seq_len % block_q != 0:
    raise ValueError(f"{q_seq_len=} must be a multiple of {block_q=}")
  if kv_seq_len % block_k != 0:
    raise ValueError(f"{kv_seq_len=} must be a multiple of {block_k=}")

  # Heuristics.
  grid_ = grid
  if grid_ is None:
    grid_ = (pl.cdiv(q_seq_len, block_q), batch_size, num_heads)

  num_warps_ = num_warps
  if num_warps_ is None:
    num_warps_ = 4 if head_dim <= 64 else 8
  kernel = functools.partial(mha_forward_kernel, sm_scale=sm_scale,
                             block_q=block_q, block_k=block_k,
                             head_dim=head_dim, causal=causal)

  in_specs: list[pl.BlockSpec | None] = [
      pl.BlockSpec((None, block_q, None, head_dim_padded),
                   lambda i, j, k: (j, i, k, 0)),
      pl.BlockSpec((None, kv_seq_len, None, head_dim_padded),
                   lambda _, j, k: (j, 0, k, 0)),
      pl.BlockSpec((None, kv_seq_len, None, head_dim_padded),
                   lambda _, j, k: (j, 0, k, 0)),
  ]
  in_specs.append(
      None
      if segment_ids is None
      else pl.BlockSpec((None, kv_seq_len), lambda _, j, k: (j, 0))
  )
  out_shape = [q]
  out_specs = [pl.BlockSpec((None, block_q, None, head_dim_padded),
                            lambda i, j, k: (j, i, k, 0))]
  if return_residuals:
    out_shape.append(jax.ShapeDtypeStruct(
        shape=(batch_size, num_heads, q_seq_len), dtype=jnp.float32))  # lse
    out_specs.append(
        pl.BlockSpec((None, None, block_q), lambda i, j, k: (j, k, i)))  # lse
  out = pl.pallas_call(
      kernel,
      grid=grid_,
      in_specs=in_specs,
      out_specs=out_specs,
      compiler_params=plgpu.CompilerParams(
          num_warps=num_warps_, num_stages=num_stages),
      out_shape=out_shape,
      debug=debug,
      interpret=interpret,
      name="mha_forward",
  )(q, k, v, segment_ids)
  return out if return_residuals else out[0]

