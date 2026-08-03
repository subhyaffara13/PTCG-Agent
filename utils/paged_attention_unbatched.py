import functools

def paged_attention_unbatched(
    q: jax.Array,  #  [num_q_heads, head_dim]
    k_pages: jax.Array,  #  [num_kv_heads, total_num_pages, page_size, head_dim]
    v_pages: jax.Array,  #  [num_kv_heads, total_num_pages, page_size, head_dim]
    block_tables: jax.Array,  #  [pages_per_sequence]
    lengths: jax.Array | None,  #  [1]
    k_scales_pages: jax.Array | None = None,  # [num_kv_heads, total_num_pages, page_size]
    v_scales_pages: jax.Array | None = None,  # [num_kv_heads, total_num_pages, page_size]
    *,
    block_h: int,
    pages_per_compute_block: int,
    k_splits: int,
    num_warps: int,
    num_stages: int,
    interpret: bool,
    debug: bool,
    mask_value: float,
    attn_logits_soft_cap: float | None,
) -> jax.Array:
  num_q_heads, head_dim = q.shape
  num_kv_heads, total_num_pages, page_size, _ = k_pages.shape
  pages_per_sequence = block_tables.shape[0]

  assert (
      pages_per_sequence % k_splits == 0
  ), f"{pages_per_sequence=} must be divisible by {k_splits=}."

  pages_per_partition = pages_per_sequence // k_splits
  pages_per_compute_block = min(pages_per_partition, pages_per_compute_block)

  assert (
      pages_per_partition % pages_per_compute_block == 0
  ), f"{pages_per_partition=} must de divisible by {pages_per_compute_block=}."

  block_tables = block_tables.reshape(k_splits, pages_per_sequence // k_splits)

  q_heads_per_kv_head = num_q_heads // num_kv_heads
  q_reshaped = q.reshape(num_kv_heads, q_heads_per_kv_head, head_dim)

  if q_heads_per_kv_head % block_h:
    q_reshaped = jnp.pad(
        q_reshaped, ((0, 0), (0, -q_heads_per_kv_head % block_h), (0, 0))
    )

  head_splits = pl.cdiv(q_heads_per_kv_head, block_h)
  grid = (num_kv_heads, head_splits, k_splits)
  kernel = functools.partial(
      paged_attention_kernel,
      num_heads=q_heads_per_kv_head,
      pages_per_compute_block=pages_per_compute_block,
      mask_value=mask_value,
      attn_logits_soft_cap=attn_logits_soft_cap,
  )
  # set up quantization scales
  if k_scales_pages is not None:
    assert k_scales_pages.shape == (num_kv_heads, total_num_pages, page_size)
    k_scales_spec = pl.BlockSpec((None, total_num_pages, page_size),
                                 lambda h, i, k: (h, 0, 0))
  else:
    k_scales_spec = None
  if v_scales_pages is not None:
    assert v_scales_pages.shape == (num_kv_heads, total_num_pages, page_size)
    v_scales_spec = pl.BlockSpec((None, total_num_pages, page_size),
                                 lambda h, i, k: (h, 0, 0))
  else:
    v_scales_spec = None

  o, l, m = pl.pallas_call(
      kernel,
      grid=grid,
      in_specs=[
          pl.BlockSpec(
              (None, block_h, head_dim), lambda h, i, k: (h, i, 0)
          ),  # q
          pl.BlockSpec(
              (None, total_num_pages, page_size, head_dim),
              lambda h, i, k: (h, 0, 0, 0),
          ),  # k_pages
          k_scales_spec,  # k_pages_scale
          pl.BlockSpec(
              (None, total_num_pages, page_size, head_dim),
              lambda h, i, k: (h, 0, 0, 0),
          ),  # v_pages
          v_scales_spec,  # v_pages_scale
          pl.BlockSpec(
              (None, pages_per_partition), lambda h, i, k: (k, 0)
          ),  # block_tables
      ]
      + [
          None if lengths is None else pl.BlockSpec((1,), lambda h, i, k: (0,))
      ],  # lengths
      out_specs=[
          pl.BlockSpec(
              (None, None, block_h, head_dim), lambda h, i, k: (k, h, i, 0)
          ),  # q
          pl.BlockSpec((None, None, block_h), lambda h, i, k: (k, h, i)),  # l
          pl.BlockSpec((None, None, block_h), lambda h, i, k: (k, h, i)),  # m
      ],
      out_shape=[
          jax.ShapeDtypeStruct(
              (k_splits, *q_reshaped.shape), dtype=q.dtype
          ),  # o
          jax.ShapeDtypeStruct(
              (k_splits, *q_reshaped.shape[:-1]), dtype=jnp.float32
          ),  # l
          jax.ShapeDtypeStruct(
              (k_splits, *q_reshaped.shape[:-1]), dtype=jnp.float32
          ),  # m
      ],
      debug=debug,
      interpret=interpret,
      compiler_params=plgpu.CompilerParams(
          num_warps=num_warps, num_stages=num_stages
      ),
      name=f"paged_attention_{block_h=}_{pages_per_compute_block=}",
  )(q_reshaped, k_pages, k_scales_pages, v_pages, v_scales_pages, block_tables, lengths)

  if q_heads_per_kv_head % block_h:
    o = o[..., :q_heads_per_kv_head, :]
    l = l[..., :q_heads_per_kv_head]
    m = m[..., :q_heads_per_kv_head]

  # final round of flash
  m_next = m.max(axis=0)
  correction = jnp.exp(m - m_next[None])
  o = o * correction[..., None].astype(o.dtype)
  l_next = (l * correction).sum(axis=0)
  eps = jnp.finfo(l_next.dtype).eps
  o = o.sum(axis=0) / ((l_next[..., None] + eps).astype(o.dtype))

  o = o.reshape(q.shape).astype(q.dtype)
  return o

