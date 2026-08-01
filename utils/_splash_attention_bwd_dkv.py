
def _splash_attention_bwd_dkv(
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
    bkv_compute: int,
    is_mqa: bool,
    mask_info: mask_info_lib.MaskInfo,
    mask_value: float,
    attn_logits_soft_cap: float | None,
    use_fused_bwd_kernel: bool,
    q_layout: QKVLayout,
    k_layout: QKVLayout,
    v_layout: QKVLayout,
    mask_function: MaskFunctionType | None,
    interpret: bool,
):
  num_q_heads, q_seq_len, head_dim_qk = q.shape
  head_dim_v = v.shape[-1]
  if is_mqa:
    num_kv_heads, kv_seq_len = 1, k.shape[0]
  else:
    num_kv_heads, kv_seq_len, _ = k.shape

  if bq > q_seq_len:
    raise ValueError(
        f"{bq=} should not be greater than {q_seq_len=}")
  if bkv > kv_seq_len:
    raise ValueError(
        f"{bkv=} should not be greater than {kv_seq_len=}")
  if bkv_compute > bkv:
    raise ValueError(
        f"{bkv_compute=} should not be greater than {bkv=}")
  if bkv % bkv_compute:
    raise ValueError(
        f"{bkv=} should be a multiple of {bkv_compute=}")

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

  q_heads_per_kv_head = num_q_heads // num_kv_heads

  if mask_info.data_next is not None:
    grid_width = mask_info.data_next.shape[-2]
  else:
    grid_width = q_seq_len // bq

  grid = (
      kv_seq_len // bkv,
      num_q_heads,
      grid_width,
  )

  def o_index_map(
      kv_index,
      head_index,
      q_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref=None,
  ):
    next_i, *_ = _next_nonzero(
        head_index,
        q_index,
        kv_index,
        data_next_ref,
        block_mask_ref,
        mask_next_ref,
        next_i=True,
    )
    return head_index, next_i, 0

  o_spec = pl.BlockSpec((None, bq, head_dim_v), o_index_map)

  def q_index_map(
      kv_index,
      head_index,
      q_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref=None,
  ):
    next_i, *_ = _next_nonzero(
        head_index,
        q_index,
        kv_index,
        data_next_ref,
        block_mask_ref,
        mask_next_ref,
        next_i=True,
    )
    return from_head_minor((head_index, next_i, 0), q_layout)

  q_spec = pl.BlockSpec(
      from_head_minor((None, bq, head_dim_qk), q_layout), q_index_map
  )

  def k_index_map(kv_index, head_index, *_):
    prefix = () if is_mqa else (_div(head_index, q_heads_per_kv_head),)
    return from_head_minor((*prefix, kv_index, 0), k_layout)

  k_spec = pl.BlockSpec(
      from_head_minor(
          (bkv, head_dim_qk) if is_mqa else (None, bkv, head_dim_qk),
          k_layout,
      ),
      k_index_map,
  )

  def v_index_map(kv_index, head_index, *_):
    prefix = () if is_mqa else (_div(head_index, q_heads_per_kv_head),)
    return from_head_minor((*prefix, kv_index, 0), v_layout)

  v_spec = pl.BlockSpec(
      from_head_minor(
          (bkv, head_dim_v) if is_mqa else (None, bkv, head_dim_v),
          v_layout,
      ),
      v_index_map,
  )

  if use_fused_bwd_kernel:
    def dq_index_map(kv_index, head_index, q_index, *_):
      return (kv_index, head_index, q_index, 0)
    dq_spec = pl.BlockSpec((None, None, bq, head_dim_qk), dq_index_map)
    dq_shape = jax.ShapeDtypeStruct((kv_seq_len // bkv, *q.shape), q.dtype)
    if bkv == bkv_compute:
      dq_scratch_spec = dq_scratch_shape = None
    else:
      dq_scratch_spec = pl.BlockSpec((bq, head_dim_qk), lambda *_: (0, 0))
      dq_scratch_shape = jax.ShapeDtypeStruct((bq, head_dim_qk), jnp.float32)
  else:
    dq_spec = dq_shape = dq_scratch_spec = dq_scratch_shape = None

  def dkv_index_map(kv_index, head_index, *_):
    prefix = () if is_mqa else (_div(head_index, q_heads_per_kv_head),)
    return (*prefix, kv_index, 0)

  dk_spec = pl.BlockSpec(
      (bkv, head_dim_qk) if is_mqa else (None, bkv, head_dim_qk),
      dkv_index_map,
  )

  dv_spec = pl.BlockSpec(
      (bkv, head_dim_v) if is_mqa else (None, bkv, head_dim_v), dkv_index_map,
  )

  def mask_index_map(
      kv_index,
      head_index,
      q_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref,
  ):
    _, next_m, *_ = _next_nonzero(
        head_index,
        q_index,
        kv_index,
        data_next_ref,
        block_mask_ref,
        mask_next_ref,
        next_i=True,
    )
    return next_m, 0, 0

  mask_spec = pl.BlockSpec((None, bkv, bq), mask_index_map)

  def q_segment_ids_index_map(
      kv_index,
      head_index,
      q_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref=None,
  ):
    next_i, *_ = _next_nonzero(
        head_index,
        q_index,
        kv_index,
        data_next_ref,
        block_mask_ref,
        mask_next_ref,
        next_i=True,
    )
    return 0, next_i

  if segment_ids is not None:
    def kv_segment_ids_index_map(kv_index, *_):
      return kv_index, 0

    q_segment_spec = pl.BlockSpec((NUM_SUBLANES, bq), q_segment_ids_index_map)
    kv_segment_spec = pl.BlockSpec((bkv, NUM_LANES), kv_segment_ids_index_map)
    q_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.q, (NUM_SUBLANES, q_seq_len), (1,)
    )
    kv_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.kv, (kv_seq_len, NUM_LANES), (0,)
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

  def logsumexp_index_map(
      kv_index,
      head_index,
      q_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref=None,
  ):
    next_i, *_ = _next_nonzero(
        head_index,
        q_index,
        kv_index,
        data_next_ref,
        block_mask_ref,
        mask_next_ref,
        next_i=True,
    )
    return head_index, 0, next_i

  assert logsumexp.shape == di.shape == (num_q_heads, q_seq_len)
  # TODO(apaszke): Remove the sublane expansion once Mosaic has all retilings
  logsumexp_shape = (num_q_heads, NUM_SUBLANES, q_seq_len)
  logsumexp = jnp.broadcast_to(jnp.expand_dims(logsumexp, -2), logsumexp_shape)
  logsumexp_spec = pl.BlockSpec((None, NUM_SUBLANES, bq), logsumexp_index_map)
  assert logsumexp_spec.block_shape is not None
  assert logsumexp.ndim == len(logsumexp_spec.block_shape)

  # TODO(apaszke): Remove the sublane expansion once Mosaic has all retilings
  di = jnp.broadcast_to(jnp.expand_dims(di, -2), logsumexp_shape)
  di_spec = pl.BlockSpec((None, NUM_SUBLANES, bq), logsumexp_index_map)
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

  if mask_info.q_sequence is not None:
    in_specs.append(pl.BlockSpec((NUM_SUBLANES, bq), q_segment_ids_index_map))
    q_sequence = jax.lax.broadcast_in_dim(
        mask_info.q_sequence, (NUM_SUBLANES, q_seq_len), (1,)
    )
  else:
    q_sequence = None
    in_specs.append(None)

  out_shapes = [
      dq_scratch_shape,
      jax.ShapeDtypeStruct((bkv, head_dim_qk), jnp.float32),
      jax.ShapeDtypeStruct((bkv, head_dim_v), jnp.float32),
      dq_shape,
      jax.ShapeDtypeStruct.like(k),
      jax.ShapeDtypeStruct.like(v),
  ]
  out_specs = [
      dq_scratch_spec,
      pl.BlockSpec((bkv, head_dim_qk), lambda *_: (0, 0)),
      pl.BlockSpec((bkv, head_dim_v), lambda *_: (0, 0)),
      dq_spec,
      dk_spec,
      dv_spec,
  ]

  kernel = functools.partial(
      _flash_attention_dkv_kernel,
      mask_value=mask_value,
      num_q_heads=num_q_heads,
      num_kv_heads=num_kv_heads,
      is_mqa=is_mqa,
      grid_width=grid_width,
      bq=bq,
      bkv_compute=bkv_compute,
      attn_logits_soft_cap=attn_logits_soft_cap,
      q_layout=q_layout,
      k_layout=k_layout,
      v_layout=v_layout,
      bkv=bkv,
      mask_function=mask_function,
  )
  num_scalar_prefetch = 3

  kernel_name = get_kernel_name(
      is_mqa=is_mqa,
      save_residuals=False,
      is_segmented=segment_ids is not None,
      phase="dkv",
  )
  metadata = {"xprof_metadata": json.dumps(dict(
      block_q_dkv=bq,
      block_kv_dkv=bkv,
      block_kv_dkv_compute=bkv_compute,
      q_layout=q_layout,
      k_layout=k_layout,
      v_layout=v_layout,
  ))}
  with jax.named_scope(kernel_name):
    _, _, _, dq_unreduced, dk, dv = pl.pallas_call(
        kernel,
        grid_spec=pltpu.PrefetchScalarGridSpec(
            num_scalar_prefetch=num_scalar_prefetch,
            in_specs=in_specs,
            out_specs=out_specs,
            grid=grid,
        ),
        out_shape=out_shapes,
        # We set all dimensions to arbitrary because:
        # 1) for kv_seq_len, the splash attention prefetch schedule assumes no
        #    megacore
        # 2) for heads, we are reducing over heads
        # 3) for q_seq_len, we are reducing over it to compute dkv
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
  if use_fused_bwd_kernel:
    assert dq_unreduced is not None
    dq = dq_unreduced.sum(axis=0)
  else:
    assert dq_unreduced is None
    dq = None
  return dq, dk, dv

