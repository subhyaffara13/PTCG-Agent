
def _splash_attention_bwd_dq(
    q,
    k,
    v,
    segment_ids,
    sinks,
    logsumexp,
    do,
    di,
    *,
    bq: int,
    bkv: int,
    is_mqa: bool,
    mask_info: mask_info_lib.MaskInfo,
    mask_value: float,
    attn_logits_soft_cap: float | None,
    q_layout: QKVLayout,
    k_layout: QKVLayout,
    v_layout: QKVLayout,
    mask_function: MaskFunctionType | None,
    interpret: bool,
):
  num_q_heads, q_seq_len, head_dim_qk = q.shape
  head_dim_v = v.shape[-1]
  if is_mqa:
    kv_seq_len = k.shape[0]
    num_kv_heads = 1
  else:
    kv_seq_len = k.shape[1]
    num_kv_heads = k.shape[0]

  if bq > q_seq_len:
    raise ValueError(
        f"{bq=} should not be greater than {q_seq_len=}")
  if bkv > kv_seq_len:
    raise ValueError(
        f"{bkv=} should not be greater than {kv_seq_len=}")

  if not is_mqa and num_q_heads % num_kv_heads != 0:
    raise ValueError(
        f"In MHA, expected number of 'key' heads ({num_kv_heads}) to be a"
        f" multiple of the number of 'query' heads ({num_q_heads})"
    )

  if k.shape[:-1] != v.shape[:-1]:
    raise ValueError(
        f"Expected 'key' {k.shape} and 'value' {v.shape} to have the same "
        "leading dimensions."
    )

  if bkv % NUM_LANES:
    raise ValueError(f"{bkv=} must be a multiple of {NUM_LANES}.")

  # TODO(amagni/sharadmv): when adding block_compute, make sure that is a
  # multiple of NUM_LANES.

  q_heads_per_kv_head = num_q_heads // num_kv_heads

  if mask_info.data_next is not None:
    grid_width = mask_info.data_next.shape[-1]
  else:
    grid_width = kv_seq_len // bkv

  grid = (num_q_heads, q_seq_len // bq, grid_width)

  def o_index_map(h, i, *_):
    return h, i, 0

  o_spec = pl.BlockSpec((None, bq, head_dim_v), o_index_map)

  def q_index_map(h, i, *_):
    return from_head_minor((h, i, 0), q_layout)

  q_spec = pl.BlockSpec(
      from_head_minor((None, bq, head_dim_qk), q_layout), q_index_map
  )

  def k_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref, *_):
    next_j, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    prefix = () if is_mqa else (_div(h, q_heads_per_kv_head),)
    return from_head_minor((*prefix, next_j, 0), k_layout)

  k_spec = pl.BlockSpec(
      from_head_minor(
          (bkv, head_dim_qk) if is_mqa else (None, bkv, head_dim_qk), k_layout
      ),
      k_index_map,
  )

  def v_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref, *_):
    next_j, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    prefix = () if is_mqa else (_div(h, q_heads_per_kv_head),)
    return from_head_minor((*prefix, next_j, 0), v_layout)

  v_spec = pl.BlockSpec(
      from_head_minor(
          (bkv, head_dim_v) if is_mqa else (None, bkv, head_dim_v), v_layout
      ),
      v_index_map,
  )

  def mask_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref, *_):
    _, next_m, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    return next_m, 0, 0

  mask_spec = pl.BlockSpec((None, bq, bkv), mask_index_map)

  def q_segment_ids_index_map(h, i, j, *_):
    del h, j  # Unused.
    return i, 0

  if segment_ids is not None:

    def kv_segment_ids_index_map(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref, *_
    ):
      next_j, *_ = _next_nonzero(
          h, i, j, data_next_ref, block_mask_ref, mask_next_ref
      )
      return 0, next_j

    q_segment_spec = pl.BlockSpec((bq, NUM_LANES), q_segment_ids_index_map)
    kv_segment_spec = pl.BlockSpec(
        (NUM_SUBLANES, bkv), kv_segment_ids_index_map
    )
    q_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.q, (q_seq_len, NUM_LANES), (0,)
    )
    kv_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.kv, (NUM_SUBLANES, kv_seq_len), (1,)
    )
  else:
    q_segment_spec = kv_segment_spec = None
    q_segment_ids = kv_segment_ids = None

  if sinks is not None:
    assert sinks.shape == (num_q_heads,)
    # align sinks to sublanes to allow vmap and shard_map over the kernel
    sinks_spec = pl.BlockSpec(
        (NUM_SUBLANES, num_q_heads), lambda h, i, j, *_: (0, 0),
        memory_space=pltpu.SMEM
    )
    sinks = jnp.broadcast_to(sinks.astype(jnp.float32)[None, :],
                             (NUM_SUBLANES, num_q_heads))
  else:
    sinks_spec = None

  do_spec = o_spec

  def logsumexp_index_map(h, i, *_):
    return h, 0, i

  logsumexp = jnp.expand_dims(logsumexp, axis=-2)
  logsumexp_spec = pl.BlockSpec((None, 1, bq), logsumexp_index_map)
  assert logsumexp_spec.block_shape is not None
  assert logsumexp.ndim == len(logsumexp_spec.block_shape)

  di = jnp.expand_dims(di, axis=-2)
  di_spec = pl.BlockSpec((None, 1, bq), logsumexp_index_map)
  assert di_spec.block_shape is not None
  assert di.ndim == len(di_spec.block_shape)

  in_specs = [
      q_spec,
      k_spec,
      v_spec,
      q_segment_spec,
      kv_segment_spec,
      sinks_spec,
      logsumexp_spec,
      do_spec,
      di_spec,
  ]
  if mask_info.partial_mask_blocks is not None:
    in_specs.append(mask_spec)
  else:
    in_specs.append(None)

  assert mask_info.partial_mask_blocks is None or mask_info.q_sequence is None

  if mask_info.q_sequence is not None:
    q_sequence = jax.lax.broadcast_in_dim(
        mask_info.q_sequence, (q_seq_len, NUM_LANES), (0,)
    )
    in_specs.append(pl.BlockSpec((bq, NUM_LANES), q_segment_ids_index_map))
  else:
    q_sequence = None
    in_specs.append(None)

  out_shapes = [
      jax.ShapeDtypeStruct((bq, head_dim_qk), jnp.float32),
      jax.ShapeDtypeStruct.like(q),
  ]
  out_specs = [
      pl.BlockSpec((bq, head_dim_qk), lambda *_: (0, 0)),
      pl.BlockSpec((None, bq, head_dim_qk), lambda h, i, *_: (h, i, 0)),
  ]

  kernel = functools.partial(
      _flash_attention_dq_kernel,
      grid_width=grid_width,
      mask_value=mask_value,
      bq=bq,
      bkv=bkv,
      attn_logits_soft_cap=attn_logits_soft_cap,
      q_layout=q_layout,
      k_layout=k_layout,
      v_layout=v_layout,
      mask_function=mask_function,
  )
  num_scalar_prefetch = 3

  kernel_name = get_kernel_name(
      is_mqa=is_mqa,
      save_residuals=False,
      is_segmented=segment_ids is not None,
      phase="dq",
  )
  metadata = {"xprof_metadata": json.dumps(dict(
      block_q_dq=bq,
      block_kv_dq=bkv,
      q_layout=q_layout,
      k_layout=k_layout,
      v_layout=v_layout,
  ))}
  with jax.named_scope(kernel_name):
    _, dq = pl.pallas_call(
        kernel,
        grid_spec=pltpu.PrefetchScalarGridSpec(
            num_scalar_prefetch=num_scalar_prefetch,
            in_specs=in_specs,
            out_specs=out_specs,
            grid=grid,
        ),
        out_shape=out_shapes,
        compiler_params=pltpu.CompilerParams(
          dimension_semantics=("arbitrary", "arbitrary", "arbitrary"),
        ),
        name=kernel_name,
        interpret=interpret,
        metadata=metadata,
    )(
        mask_info.data_next,
        mask_info.block_mask,
        mask_info.mask_next,
        q if q_layout == QKVLayout.HEAD_DIM_MINOR else q.swapaxes(-1, -2),
        k if k_layout == QKVLayout.HEAD_DIM_MINOR else k.swapaxes(-1, -2),
        v if v_layout == QKVLayout.HEAD_DIM_MINOR else v.swapaxes(-1, -2),
        q_segment_ids,
        kv_segment_ids,
        sinks,
        logsumexp,
        do,
        di,
        mask_info.partial_mask_blocks,
        q_sequence,
    )
  return dq

