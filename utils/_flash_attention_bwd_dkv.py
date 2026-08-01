
def _flash_attention_bwd_dkv(
    q,
    k,
    v,
    ab,
    segment_ids,
    l,
    m,
    do,
    di,
    *,
    block_q_major: int,
    block_q: int,
    block_k_major: int,
    block_k: int,
    sm_scale: float,
    causal: bool = False,
    mask_value: float = DEFAULT_MASK_VALUE,
    debug: bool = False,
):
  batch_size, num_heads, q_seq_len, head_dim = q.shape
  _, _, kv_seq_len, _ = k.shape
  _verify_block("block_q_major_dkv", "q_seq_len", block_q_major, q_seq_len)
  _verify_block("block_q_dkv", "q_seq_len", block_q, q_seq_len)
  _verify_block("block_k_major_dkv", "kv_seq_len", block_k_major, kv_seq_len)
  _verify_block("block_k_dkv", "kv_seq_len", block_k, kv_seq_len)

  # Broadcast out scalar values
  m = jnp.broadcast_to(m[..., None], (*m.shape, MIN_BLOCK_SIZE))
  l = jnp.broadcast_to(l[..., None], (*l.shape, MIN_BLOCK_SIZE))
  # Preprocess contraction for bwd pass
  di = jnp.broadcast_to(di[..., None], (*di.shape, MIN_BLOCK_SIZE))

  # kv index needs to be before q index since q index is the contractng
  # dimension.
  grid = (
      batch_size,
      num_heads,
      kv_seq_len // block_k_major,
      q_seq_len // block_q_major,
  )

  def qo_index_map(batch_index, head_index, kv_seq_index, q_seq_index):
    if causal:
      # If the q block is skipped, stay at the 0th q block.
      next_q_index = lax.select(
          below_or_on_diag(
              q_seq_index, block_q_major, kv_seq_index, block_k_major
          ),
          q_seq_index,
          0,
      )
    else:
      next_q_index = q_seq_index

    return (batch_index, head_index, next_q_index, 0)

  qo_spec = pl.BlockSpec((1, 1, block_q_major, head_dim), qo_index_map)
  assert qo_spec.block_shape is not None
  assert q.ndim == len(qo_spec.block_shape)
  do_spec = qo_spec
  assert do.ndim == len(qo_spec.block_shape)

  def kv_index_map(batch_index, head_index, kv_seq_index, _):
    return (batch_index, head_index, kv_seq_index, 0)

  kv_spec = pl.BlockSpec((1, 1, block_k_major, head_dim), kv_index_map)
  assert kv_spec.block_shape is not None
  assert k.ndim == len(kv_spec.block_shape)
  assert v.ndim == len(kv_spec.block_shape)

  def lm_index_map(batch_index, head_index, _, q_seq_index):
    return (batch_index, head_index, q_seq_index, 0)

  lm_spec = pl.BlockSpec((1, 1, block_q_major, MIN_BLOCK_SIZE), lm_index_map)
  assert lm_spec.block_shape is not None
  assert l.ndim == len(lm_spec.block_shape)
  assert m.ndim == len(lm_spec.block_shape)

  di_spec = pl.BlockSpec((1, 1, block_q_major, MIN_BLOCK_SIZE), qo_index_map)
  assert di_spec.block_shape is not None
  assert di.ndim == len(di_spec.block_shape)

  def ab_index_map(batch_index, head_index, kv_seq_index, q_seq_index):
    return (batch_index, head_index, q_seq_index, kv_seq_index)

  dab_spec = (
      pl.BlockSpec((1, 1, block_q_major, block_k_major), ab_index_map)
      if ab is not None
      else None
  )

  q_segment_ids_spec = kv_segment_ids_spec = None
  q_segment_ids = kv_segment_ids = None
  if segment_ids is not None:

    def q_segment_ids_index_map(
        batch_index, head_index, kv_seq_index, q_seq_index
    ):
      del head_index
      if causal:
        next_q_index = lax.select(
            below_or_on_diag(
                q_seq_index, block_q_major, kv_seq_index, block_k_major
            ),
            q_seq_index,
            0,
        )
      else:
        next_q_index = q_seq_index
      return (batch_index, next_q_index, 0)

    def kv_segment_ids_index_map(batch_index, head_index, kv_seq_index, _):
      del head_index
      return (batch_index, 0, kv_seq_index)

    q_segment_ids_spec = pl.BlockSpec(
        (1, block_q_major, NUM_LANES), q_segment_ids_index_map
    )
    kv_segment_ids_spec = pl.BlockSpec(
        (1, NUM_SUBLANES, block_k_major), kv_segment_ids_index_map
    )

    q_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.q,
        (batch_size, q_seq_len, NUM_LANES),
        (
            0,
            1,
        ),
    )
    kv_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.kv,
        (batch_size, NUM_SUBLANES, kv_seq_len),
        (
            0,
            2,
        ),
    )

  in_specs = [
      qo_spec,
      kv_spec,
      kv_spec,
      dab_spec,
      q_segment_ids_spec,
      kv_segment_ids_spec,
      lm_spec,
      lm_spec,
      do_spec,
      di_spec,
  ]

  out_shapes = [
      jax.ShapeDtypeStruct((batch_size, num_heads, kv_seq_len, head_dim),
                           k.dtype),
      jax.ShapeDtypeStruct((batch_size, num_heads, kv_seq_len, head_dim),
                           v.dtype),
  ]
  def dkv_index_map(batch_index, head_index, kv_seq_index, _):
    return (batch_index, head_index, kv_seq_index, 0)

  dkv_spec = pl.BlockSpec((1, 1, block_k_major, head_dim), dkv_index_map)
  out_specs = [dkv_spec, dkv_spec]
  scratch_shapes = [
      pltpu.VMEM((block_k_major, head_dim), jnp.float32),
      pltpu.VMEM((block_k_major, head_dim), jnp.float32),
  ]

  kernel = functools.partial(
      _flash_attention_dkv_kernel,
      block_q=block_q,
      block_k=block_k,
      sm_scale=sm_scale,
      causal=causal,
      mask_value=mask_value,
      q_seq_len=q_seq_len,
  )
  name_scope = f"flash_mha_bwd_dkv_{block_q_major=}_{block_q=}_{block_k_major=}_{block_k=}"
  with jax.named_scope(name_scope):
    dk, dv = pl.pallas_call(
        kernel,
        grid_spec=pltpu.PrefetchScalarGridSpec(
            num_scalar_prefetch=0,
            grid=grid,
            in_specs=in_specs,
            out_specs=out_specs,
            scratch_shapes=scratch_shapes,
        ),
        out_shape=out_shapes,
        debug=debug,
        compiler_params=pltpu.CompilerParams(
                dimension_semantics=(
                    "parallel",
                    "parallel",
                    "parallel",
                    "arbitrary",
                )
        ),
    )(q, k, v, ab, q_segment_ids, kv_segment_ids, l, m, do, di)
    assert dk.shape == k.shape
    assert dv.shape == v.shape
  return dk, dv

