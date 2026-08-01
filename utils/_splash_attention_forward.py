
def _splash_attention_forward(
    fwd_mask_info: mask_info_lib.MaskInfo,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    is_mqa: bool,
    block_sizes: BlockSizes,
    residual_checkpoint_name: str | None,
    save_residuals: Literal[False],
    mask_function: MaskFunctionType | None,
    attn_logits_soft_cap: float | None = None,
    interpret: bool = False,
) -> jax.Array:
  ...


def _splash_attention_forward(
    fwd_mask_info: mask_info_lib.MaskInfo,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    is_mqa: bool,
    block_sizes: BlockSizes,
    residual_checkpoint_name: str | None,
    save_residuals: Literal[True],
    mask_function: MaskFunctionType | None,
    attn_logits_soft_cap: float | None = None,
    interpret: bool = False,
) -> SplashCustomReturnType:
  ...


def _splash_attention_forward(
    fwd_mask_info: mask_info_lib.MaskInfo,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    is_mqa: bool,
    block_sizes: BlockSizes,
    residual_checkpoint_name: str | None,
    save_residuals: bool,
    mask_function: MaskFunctionType | None,
    attn_logits_soft_cap: float | None = None,
    interpret: bool = False
) -> SplashCustomReturnType:
  num_q_heads, q_seq_len, head_dim_qk = q.shape
  head_dim_v = v.shape[-1]
  bq, bkv = block_sizes.block_q, block_sizes.block_kv
  bkv_compute = block_sizes.block_kv_compute

  if is_mqa:
    expected_kv_rank = 2
    kv_head_dimension = 1
    kv_seq_len_dimension = 0
    num_kv_heads = 1
  else:
    expected_kv_rank = 3
    kv_head_dimension = 2
    kv_seq_len_dimension = 1
    num_kv_heads = k.shape[0]

  partial_mask_blocks = fwd_mask_info.partial_mask_blocks
  if (
      partial_mask_blocks is not None
      and jnp.dtype(partial_mask_blocks.dtype) != np.bool_
  ):
    raise ValueError(
        "partial_mask_blocks must be of type np.bool_ but got"
        f" {partial_mask_blocks.dtype}"
    )

  if len(k.shape) != expected_kv_rank:
    raise ValueError(
        f"Expected {expected_kv_rank}-dim 'key' tensor for MQA. Instead got a"
        f" {len(k.shape)}-dim one."
    )

  if k.shape[kv_head_dimension] != head_dim_qk:
    raise ValueError(
        f"Expected 'key' head dimension to be: {head_dim_qk}. Instead got:"
        f" {k.shape[kv_head_dimension]}."
    )

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

  assert bkv_compute is not None
  if bkv % bkv_compute:
    raise ValueError(f"{bkv=} must be a multiple of {bkv_compute=}.")
  if bkv_compute % NUM_LANES:
    raise ValueError(f"{bkv_compute=} must be a multiple of {NUM_LANES}.")

  kv_seq_len = k.shape[kv_seq_len_dimension]

  q_heads_per_kv_head = num_q_heads // num_kv_heads

  if segment_ids is not None:
    if segment_ids.q.shape != (q_seq_len,):
      raise ValueError(
          "Invalid shape for q segment_ids: "
          f"{segment_ids.q.shape}. Expected: {(q_seq_len,)}"
      )
    if segment_ids.kv.shape != (kv_seq_len,):
      raise ValueError(
          "Invalid shape for kv segment_ids: "
          f"{segment_ids.kv.shape}. Expected: {(kv_seq_len,)}"
      )

  q_layout = block_sizes.q_layout
  def q_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref=None):
    del j, data_next_ref, mask_next_ref, block_mask_ref
    return from_head_minor((h, i, 0), q_layout)
  def out_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref=None):
    del j, data_next_ref, mask_next_ref, block_mask_ref
    return h, i, 0

  k_layout = block_sizes.k_layout
  def k_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref=None):
    next_j, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    prefix = () if is_mqa else (_div(h, q_heads_per_kv_head),)
    return from_head_minor((*prefix, next_j, 0), k_layout)

  v_layout = block_sizes.v_layout
  def v_index_map(h, i, j, data_next_ref, block_mask_ref, mask_next_ref=None):
    next_j, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    prefix = () if is_mqa else (_div(h, q_heads_per_kv_head),)
    return from_head_minor((*prefix, next_j, 0), v_layout)

  def mask_index_map(h, i, j, data_next_ref, block_mask_ref,
                     mask_next_ref=None):
    _, next_m, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    return next_m, 0, 0

  def q_segment_ids_index_map(h, i, j, *_):
    del h, j  # Unused.
    return i, 0

  def kv_segment_ids_index_map(h, i, j, data_next_ref, block_mask_ref,
                               mask_next_ref=None):
    next_j, *_ = _next_nonzero(
        h, i, j, data_next_ref, block_mask_ref, mask_next_ref
    )
    return 0, next_j

  # Convert the logical shape from head-minor to sequence-minor.
  in_specs: list[pl.BlockSpec | None] = [
      pl.BlockSpec(
          from_head_minor((None, bq, head_dim_qk), q_layout),
          q_index_map
      ),
      pl.BlockSpec(
          from_head_minor(
              (bkv, head_dim_qk)
              if is_mqa else (None, bkv, head_dim_qk), k_layout
          ),
          k_index_map,
      ),
      pl.BlockSpec(
          from_head_minor(
              (bkv, head_dim_v) if is_mqa else (None, bkv, head_dim_v), v_layout
          ),
          v_index_map,
      ),
  ]
  if segment_ids is not None:
    in_specs += [
        pl.BlockSpec((bq, NUM_LANES), q_segment_ids_index_map),
        pl.BlockSpec((NUM_SUBLANES, bkv), kv_segment_ids_index_map),
    ]
    q_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.q, (q_seq_len, NUM_LANES), (0,)
    )
    kv_segment_ids = jax.lax.broadcast_in_dim(
        segment_ids.kv, (NUM_SUBLANES, kv_seq_len), (1,)
    )
  else:
    in_specs += [None, None]
    q_segment_ids = kv_segment_ids = None

  if sinks is not None:
    assert sinks.shape == (num_q_heads,)
    # align sinks to sublanes to allow vmap and shard_map over the kernel
    in_specs += [
        pl.BlockSpec((NUM_SUBLANES, num_q_heads), lambda h, i, j, *_: (0, 0),
                     memory_space=pltpu.SMEM)
    ]
    sinks = jnp.broadcast_to(sinks.astype(jnp.float32)[None, :],
                             (NUM_SUBLANES, num_q_heads))
  else:
    in_specs += [None]

  if fwd_mask_info.partial_mask_blocks is not None:
    in_specs.append(pl.BlockSpec((None, bq, bkv), mask_index_map))
  else:
    in_specs.append(None)

  assert (
      fwd_mask_info.partial_mask_blocks is None
      or fwd_mask_info.q_sequence is None
  )

  if fwd_mask_info.q_sequence is not None:
    q_sequence = jax.lax.broadcast_in_dim(
        fwd_mask_info.q_sequence, (q_seq_len, NUM_LANES), (0,)
    )
    in_specs.append(pl.BlockSpec((bq, NUM_LANES), q_segment_ids_index_map))
  else:
    q_sequence = None
    in_specs.append(None)

  num_scalar_prefetch = 3

  out_shapes = [
      jax.ShapeDtypeStruct((bq, NUM_LANES), jnp.float32),  # m_scratch
      jax.ShapeDtypeStruct((bq, NUM_LANES), jnp.float32),  # l_scratch
      jax.ShapeDtypeStruct((bq, head_dim_v), jnp.float32),  # o_scratch
      jax.ShapeDtypeStruct((num_q_heads, q_seq_len, head_dim_v), q.dtype),
  ]
  out_specs = [
      # TODO(sharadmv): convert m/l to be scratch
      pl.BlockSpec((bq, NUM_LANES), lambda h, i, j, *_: (0, 0)),
      pl.BlockSpec((bq, NUM_LANES), lambda h, i, j, *_: (0, 0)),
      pl.BlockSpec((bq, head_dim_v), lambda h, i, j, *_: (0, 0)),
      pl.BlockSpec((None, bq, head_dim_v), out_index_map),
  ]
  if save_residuals:
    out_shapes += [
        jax.ShapeDtypeStruct(
            (num_q_heads, q_seq_len, NUM_LANES), jnp.float32
        ),  # logsumexp
    ]

    def logsumexp_index_map(h, i, *_):
      return h, i, 0

    out_specs += [
        pl.BlockSpec((None, bq, NUM_LANES), logsumexp_index_map),
    ]
  else:
    out_shapes += [None]
    out_specs += [None]

  kernel_name = get_kernel_name(
      is_mqa=is_mqa,
      save_residuals=save_residuals,
      is_segmented=segment_ids is not None,
      phase="fwd",
  )
  metadata = {"xprof_metadata": json.dumps(dataclasses.asdict(block_sizes))}

  if fwd_mask_info.data_next is not None:
    grid_width = fwd_mask_info.data_next.shape[-1]
  else:
    grid_width = kv_seq_len // bkv

  grid = (num_q_heads, q_seq_len // bq, grid_width)
  with jax.named_scope(kernel_name):
    all_out = pl.pallas_call(
        partial(
            flash_attention_kernel,
            mask_value=mask_value,
            grid_width=grid_width,
            bq=bq,
            bkv=bkv,
            bkv_compute=bkv_compute,
            head_dim_v=head_dim_v,
            q_layout=q_layout,
            k_layout=k_layout,
            v_layout=v_layout,
            attn_logits_soft_cap=attn_logits_soft_cap,
            mask_function=mask_function,
        ),
        grid_spec=pltpu.PrefetchScalarGridSpec(
            num_scalar_prefetch=num_scalar_prefetch,
            in_specs=in_specs,
            out_specs=out_specs,
            grid=grid,
        ),
        compiler_params=pltpu.CompilerParams(
          dimension_semantics=("parallel", "arbitrary", "arbitrary"),
        ),
        out_shape=out_shapes,
        name=kernel_name,
        interpret=interpret,
        metadata=metadata,
    )(
        fwd_mask_info.data_next,
        fwd_mask_info.block_mask,
        fwd_mask_info.mask_next,
        q if q_layout == QKVLayout.HEAD_DIM_MINOR else q.swapaxes(-1, -2),
        k if k_layout == QKVLayout.HEAD_DIM_MINOR else k.swapaxes(-1, -2),
        v if v_layout == QKVLayout.HEAD_DIM_MINOR else v.swapaxes(-1, -2),
        q_segment_ids,
        kv_segment_ids,
        sinks,
        fwd_mask_info.partial_mask_blocks,
        q_sequence,
    )

  (
      _,
      _,
      _,
      out,
      logsumexp,
  ) = all_out

  if save_residuals:
    assert logsumexp is not None
    logsumexp = logsumexp[..., 0]

  if residual_checkpoint_name is not None:
    out = ad_checkpoint.checkpoint_name(out, name=residual_checkpoint_name)
    if logsumexp is not None:
      logsumexp = ad_checkpoint.checkpoint_name(
          logsumexp, name=residual_checkpoint_name
      )
  if save_residuals:
    return out, (logsumexp,)
  return out

