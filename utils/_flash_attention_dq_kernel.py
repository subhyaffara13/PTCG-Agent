
def _flash_attention_dq_kernel(
    q_tile_ref,
    k_tile_ref,
    v_tile_ref,
    ab_tile_ref,
    q_segment_ids_tile_ref,
    kv_segment_ids_tile_ref,
    l_tile_ref,
    m_tile_ref,
    do_tile_ref,
    di_tile_ref,
    dq_tile_ref,
    ds_tile_ref,
    dq_scratch_ref,
    *,
    sm_scale: float,
    causal: bool,
    mask_value: float,
    kv_seq_len: int,
    block_k: int,
):
  _, _, block_k_major, _ = k_tile_ref.shape
  _, _, block_q_major, _ = q_tile_ref.shape

  kv_seq_index = pl.program_id(axis=3)
  q_seq_index = pl.program_id(axis=2)

  @pl.when(kv_seq_index == 0)
  def start_new_sequence():
    dq_scratch_ref[:, :] = jnp.zeros(dq_scratch_ref.shape, dq_scratch_ref.dtype)

  def body(i, _):
    k_slice = pl.ds(i * block_k, block_k)
    q = q_tile_ref[0, 0, :, :]
    k = k_tile_ref[0, 0, k_slice, :]  # [block_k, head_dim]
    v = v_tile_ref[0, 0, k_slice, :]  # [block_k, head_dim]
    l = l_tile_ref[0, 0, :, :]  # [block_q_major, 128]
    m = m_tile_ref[0, 0, :, :]  # [block_q_major, 128]
    do = do_tile_ref[0, 0, :, :]  # [block_q_major, head_dim]
    di = di_tile_ref[0, 0, :].astype(jnp.float32)  # [block_q_major, 128]

    capped_logits = jax.lax.dot_general(
        q, k, TRANS_B_DIM_NUMBERS, preferred_element_type=jnp.float32
    )

    if ab_tile_ref is not None:
      ab = ab_tile_ref[0, 0, :, pl.dslice(i * block_k, block_k)].astype(
          jnp.float32
      )
      capped_logits += ab

    if sm_scale != 1.0:
      capped_logits *= sm_scale

    mask = None
    if q_segment_ids_tile_ref is not None:
      repeats, rem = divmod(block_k, NUM_LANES)
      if rem:
        raise NotImplementedError(
            f"kv block size must be a multiple of {NUM_LANES}"
        )
      q_segment_ids = jnp.tile(
          q_segment_ids_tile_ref[0], (1, repeats)
      )  # [block_q, block_k].
      kv_segment_ids = kv_segment_ids_tile_ref[:, 0, k_slice]  # [1, block_k].
      mask = jnp.equal(q_segment_ids, kv_segment_ids).astype(jnp.bool_)

    if causal:
      mask_shape = (block_q_major, block_k)
      row_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 0)
      row_ids += q_seq_index * block_q_major
      col_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 1)
      col_ids += kv_seq_index * block_k_major + i * block_k
      causal_mask = col_ids <= row_ids
      mask = causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
    capped_logits = (
        capped_logits
        if mask is None
        else capped_logits + jnp.where(mask, 0.0, mask_value)
    )

    p = jnp.exp(
        capped_logits - jnp.tile(m, (1, block_k // MIN_BLOCK_SIZE))
    )
    p = p * jnp.tile(
        1 / l, (1, block_k // MIN_BLOCK_SIZE)
    )  # [block_q_major, block_k]

    # di: [block_q_major, 128]
    # do: [block_q_major, head_dim]
    # v: [block_k_major, head_dim]
    dp = jax.lax.dot_general(
        do,
        v,
        TRANS_B_DIM_NUMBERS,
        preferred_element_type=jnp.float32,
    )
    ds = (dp - jnp.tile(di, (1, block_k // MIN_BLOCK_SIZE))) * p
    # dp = jnp.dot(do, v.T)
    # ds = (dp - (dp * p).sum(axis=1)[:, None]) * p

    if sm_scale != 1.0:
      ds = ds * sm_scale

    if ds_tile_ref is not None:
      ds_tile_ref[0, 0, :, pl.dslice(i * block_k, block_k)] = ds.astype(
          ds_tile_ref.dtype
      )

    # dp: [block_q_major, block_k]
    # k: [block_k, head_dim]
    dq_scratch_ref[:, :] += lax.dot(
        ds.astype(k.dtype),
        k,
        preferred_element_type=jnp.float32,
    ).astype(dq_scratch_ref.dtype)

  if causal:
    should_run = below_or_on_diag(
        q_seq_index, block_q_major, kv_seq_index, block_k_major
    )
    should_not_run = lax.select(should_run, False, True)
  else:
    should_run = True
    should_not_run = False

  @pl.when(should_run)
  def run():
    lax.fori_loop(0, block_k_major // block_k, body, None, unroll=True)

  @pl.when(should_not_run)
  def zero_out_ds():
    if ds_tile_ref is not None:
      ds_tile_ref[...] = jnp.zeros_like(ds_tile_ref)

  @pl.when(kv_seq_index == kv_seq_len // block_k_major - 1)
  def end_of_kv_sequence():
    dq_tile_ref[0, 0, :, :] = dq_scratch_ref[...].astype(dq_tile_ref.dtype)
    dq_scratch_ref[...] = jnp.zeros_like(dq_scratch_ref)


def _flash_attention_dq_kernel(
    # Prefetched inputs
    data_next_ref,
    block_mask_ref,
    mask_next_ref,
    # Inputs
    q_ref,
    k_ref,
    v_ref,
    q_segment_ids_ref,
    kv_segment_ids_ref,
    sinks_ref,
    logsumexp_ref,
    do_ref,
    di_ref,
    mask_ref,
    q_sequence_ref,
    # Outputs
    dq_scratch_ref,
    dq_ref,
    *,
    mask_value: float,
    grid_width: int,
    bq: int,
    bkv: int,
    attn_logits_soft_cap: float | None = None,
    q_layout: QKVLayout,
    k_layout: QKVLayout,
    v_layout: QKVLayout,
    mask_function: MaskFunctionType | None,
):
  del sinks_ref  # potentially fuse dsinks computation into the kernel later
  float32 = jnp.float32
  HEAD_DIM_MINOR = QKVLayout.HEAD_DIM_MINOR

  h, i, j = pl.program_id(0), pl.program_id(1), pl.program_id(2)
  @pl.when(j == 0)
  def init():
    dq_scratch_ref[...] = jnp.zeros_like(dq_scratch_ref)

  global_kv_index, _, should_run, should_not_mask = _next_nonzero(
      h, i, j, data_next_ref, block_mask_ref, mask_next_ref
  )
  @pl.when(should_run)
  def run():
    q = q_ref[...] if q_layout == HEAD_DIM_MINOR else q_ref[...].T
    # We keep k and v possibly transposed, since they are RHS of dots.
    k = k_ref[...]
    v = v_ref[...]
    logsumexp = jnp.expand_dims(logsumexp_ref[0], -1)
    do = do_ref[...]
    di = jnp.expand_dims(di_ref[0], -1)

    qk_dims = NT_DIM_NUMBERS if k_layout == HEAD_DIM_MINOR else NN_DIM_NUMBERS
    qk_uncapped = lax.dot_general(q, k, qk_dims, preferred_element_type=float32)

    k_slice = pl.ds(0, bkv)
    assert isinstance(k_slice, pl.Slice)
    qk = _apply_mask_and_soft_cap(
        qk_uncapped,
        mask_value,
        should_not_mask,
        mask_ref,
        q_sequence_ref,
        q_segment_ids_ref,
        kv_segment_ids_ref,
        attn_logits_soft_cap=attn_logits_soft_cap,
        k_slice=k_slice,
        # When the iteration space is shrunk (for local attention for example),
        # the kv_index program_id does not correspond to the actual coordinates
        # of the KV data. Make sure to use the 'unshrunk' index (coming from the
        # data_next array) when computing the mask.
        k_offset=global_kv_index * bkv,
        bq=bq,
        mask_function=mask_function,
    )
    p = jnp.exp(qk - logsumexp)
    dp_dims = NT_DIM_NUMBERS if v_layout == HEAD_DIM_MINOR else NN_DIM_NUMBERS
    dp = lax.dot_general(
        do.astype(v.dtype), v, dp_dims, preferred_element_type=jnp.float32,
    )
    ds = (dp - di) * p
    if attn_logits_soft_cap is not None:
      normalized = qk_uncapped / attn_logits_soft_cap
      d = jnp.tanh(normalized)
      g = ds * (1 - d)
      ds = g + g * d

    dq_dims = NN_DIM_NUMBERS if k_layout == HEAD_DIM_MINOR else NT_DIM_NUMBERS
    dq_scratch_ref[...] += lax.dot_general(
        ds.astype(k.dtype), k, dq_dims,
        preferred_element_type=jnp.float32,
    )

  @pl.when(j == grid_width - 1)
  def end():
    dq_ref[...] = dq_scratch_ref[...].astype(dq_ref.dtype)
    dq_scratch_ref[...] = jnp.zeros_like(dq_scratch_ref)

