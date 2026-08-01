
def _flash_attention_dkv_kernel(
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
    dk_tile_ref,
    dv_tile_ref,
    dk_scratch_ref,
    dv_scratch_ref,
    *,
    sm_scale: float,
    causal: bool,
    mask_value: float,
    q_seq_len: int,
    block_q: int,
    block_k: int,
):
  _, _, block_q_major, _ = q_tile_ref.shape
  _, _, block_k_major, _ = k_tile_ref.shape

  q_seq_index = pl.program_id(axis=3)
  kv_seq_index = pl.program_id(axis=2)

  @pl.when(q_seq_index == 0)
  def start_new_sequence():
    dk_scratch_ref[:, :] = jnp.zeros(dk_scratch_ref.shape, dk_scratch_ref.dtype)
    dv_scratch_ref[:, :] = jnp.zeros(dv_scratch_ref.shape, dv_scratch_ref.dtype)

  def q_body(j, _):
    start_q = j * block_q
    def k_body(i, _):
      start_k = i * block_k
      k = k_tile_ref[0, 0, pl.ds(start_k, block_k), :]
      v = v_tile_ref[0, 0, pl.ds(start_k, block_k), :]
      q = q_tile_ref[0, 0, pl.ds(start_q, block_q), :]  # [block_q, head_dim]
      l = l_tile_ref[0, 0, pl.ds(start_q, block_q), :]  # [block_q, 128]
      m = m_tile_ref[0, 0, pl.ds(start_q, block_q), :]  # [block_q, 128]
      do = do_tile_ref[0, 0, pl.ds(start_q, block_q), :]  # [block_q, 128]
      di = di_tile_ref[0, 0, pl.ds(start_q, block_q), :].astype(
          jnp.float32
      )  # [block_q, 128]

      capped_logits = lax.dot_general(
          q, k, TRANS_B_DIM_NUMBERS, preferred_element_type=jnp.float32
      )  # [block_q_major, block_k]

      if ab_tile_ref is not None:
        ab = ab_tile_ref[
            0,
            0,
            pl.dslice(j * block_q, block_q),
            pl.dslice(i * block_k, block_k),
        ].astype(jnp.float32)
        capped_logits += ab

      if sm_scale != 1.0:
        capped_logits *= sm_scale

      mask = None
      if q_segment_ids_tile_ref is not None:
        repeats, rem = divmod(block_k, NUM_LANES)
        if rem:
          raise NotImplementedError(
          )
        q_segment_ids = q_segment_ids_tile_ref[
            0, pl.ds(start_q, block_q), :
        ]  # [block_q, NUM_LANES].
        q_segment_ids = jnp.tile(
            q_segment_ids, (1, repeats)
        )  # [block_q, block_k].
        kv_segment_ids = kv_segment_ids_tile_ref[
            :, 0, pl.ds(start_k, block_k)
        ]  # [1, block_k].
        mask = jnp.equal(q_segment_ids, kv_segment_ids).astype(jnp.bool_)

      if causal:
        mask_shape = (block_q, block_k)
        row_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 0)
        row_ids += q_seq_index * block_q_major + start_q
        col_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 1)
        col_ids += kv_seq_index * block_k_major + start_k
        causal_mask = col_ids <= row_ids
        mask = (
            causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
        )

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
      )  # [block_q_major, block_k_major]
      dv = lax.dot(p.T.astype(do.dtype), do, preferred_element_type=jnp.float32)
      dv_scratch_ref[pl.ds(start_k, block_k), :] += dv.astype(
          dv_scratch_ref.dtype
      )

      # di: [block_q, 128]
      # do: [block_q, head_dim]
      # v: [block_k_major, head_dim]
      dp = lax.dot_general(
          do, v, TRANS_B_DIM_NUMBERS, preferred_element_type=jnp.float32
      )
      ds = (dp - jnp.tile(di, (1, block_k // MIN_BLOCK_SIZE))) * p

      if sm_scale != 1.0:
        ds = ds * sm_scale

      # ds: [block_q_major, block_k_major]
      # q: [block_q_major, head_dim]
      dk = lax.dot(ds.T.astype(do.dtype), q, preferred_element_type=jnp.float32)
      dk_scratch_ref[pl.ds(start_k, block_k), :] += dk.astype(
          dk_scratch_ref.dtype
      )
    lax.fori_loop(0, block_k_major // block_k, k_body, None, unroll=True)

  if causal:
    should_run = below_or_on_diag(
        q_seq_index, block_q_major, kv_seq_index, block_k_major
    )
  else:
    should_run = True

  @pl.when(should_run)
  def run():
    lax.fori_loop(0, block_q_major // block_q, q_body, None, unroll=True)

  @pl.when(q_seq_index == q_seq_len // block_q_major - 1)
  def end_of_q_sequence():
    dv_tile_ref[0, 0, :, :] = dv_scratch_ref[...].astype(dv_tile_ref.dtype)
    dk_tile_ref[0, 0, :, :] = dk_scratch_ref[...].astype(dk_tile_ref.dtype)


def _flash_attention_dkv_kernel(
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
    dk_scratch_ref,
    dv_scratch_ref,
    dq_ref,
    dk_ref,
    dv_ref,
    *,
    num_q_heads: int,
    num_kv_heads: int,
    mask_value: float,
    grid_width: int,
    bq: int,
    bkv_compute: int,
    is_mqa: bool,
    attn_logits_soft_cap: float | None,
    q_layout: QKVLayout,
    k_layout: QKVLayout,
    v_layout: QKVLayout,
    bkv: int,
    mask_function: MaskFunctionType | None,
):
  del sinks_ref  # potentially fuse dsinks computation into the kernel later
  HEAD_DIM_MINOR = QKVLayout.HEAD_DIM_MINOR
  kv_index, q_head_index, q_index = (
      pl.program_id(0),
      pl.program_id(1),
      pl.program_id(2),
  )
  should_initialize = q_index == 0

  q_heads_per_kv_heads = None
  q_head_index_per_kv_head = None

  # Consider this situation:
  # Q_heads:   0, 1, 2, 3, 4, 5, 6, 7
  # KV_heads:  0,    1,    2,    3
  # The gradient scratch buffers should be initialized for Q_heads 0, 2, 4, 6
  # (first Q_heads to 'see' a new KV_head).
  # The gradient output buffers should be written for Q_heads 1, 3, 5, 7 (last
  # Q_heads to 'see' the current KV_head).

  # We can use the same logic for both MQA and GA (grouped attention).
  # But for MQA there is no need for the rem instruction, so we skip it.
  if is_mqa:
    should_initialize = jnp.logical_and(should_initialize, q_head_index == 0)
  elif num_kv_heads < num_q_heads:
    q_heads_per_kv_heads = num_q_heads // num_kv_heads
    q_head_index_per_kv_head = lax.rem(q_head_index, q_heads_per_kv_heads)
    should_initialize = jnp.logical_and(
        should_initialize, q_head_index_per_kv_head == 0
    )
  @pl.when(should_initialize)
  def init():
    dk_scratch_ref[...] = jnp.zeros_like(dk_scratch_ref)
    dv_scratch_ref[...] = jnp.zeros_like(dv_scratch_ref)

  _, _, should_run, should_not_mask = _next_nonzero(
      q_head_index,
      q_index,
      kv_index,
      data_next_ref,
      block_mask_ref,
      mask_next_ref,
      next_i=True,
  )

  def body(i, _):

    slice_k = pl.ds(i * bkv_compute, bkv_compute)
    q = q_ref[...]  # We keep q potentially transposed, since it's always RHS
    def _load_kv(ref, layout):
      if layout == HEAD_DIM_MINOR:
        return ref[slice_k, :]
      return ref[:, slice_k].T
    k = _load_kv(k_ref, k_layout)
    v = _load_kv(v_ref, v_layout)
    logsumexp = logsumexp_ref[:1, :]
    do = do_ref[...]
    di = di_ref[:1, :]

    qk_dims = NT_DIM_NUMBERS if q_layout == HEAD_DIM_MINOR else NN_DIM_NUMBERS
    qk_uncapped = lax.dot_general(
        k, q, qk_dims, preferred_element_type=jnp.float32
    )

    assert isinstance(slice_k, pl.Slice)
    qk = _apply_mask_and_soft_cap(
        qk_uncapped,
        mask_value,
        should_not_mask,
        mask_ref,
        q_sequence_ref,
        q_segment_ids_ref,
        kv_segment_ids_ref,
        attn_logits_soft_cap=attn_logits_soft_cap,
        k_slice=slice_k,
        k_offset=kv_index * bkv + i * bkv_compute,
        bq=bq,
        k_in_lanes=False,
        mask_function=mask_function,
    )
    p = jnp.exp(qk - logsumexp)
    dv = lax.dot(p.astype(do.dtype), do, preferred_element_type=jnp.float32)
    dv = dv.astype(dv_scratch_ref.dtype) + dv_scratch_ref[slice_k, :]
    dv_scratch_ref[slice_k, :] = dv

    dp = lax.dot_general(
        v, do, NT_DIM_NUMBERS,
        preferred_element_type=jnp.float32,
    )
    ds = (dp - di) * p
    if attn_logits_soft_cap is not None:
      normalized = qk_uncapped / attn_logits_soft_cap
      d = jnp.tanh(normalized)
      g = ds * (1 - d)
      ds = g + g * d
    dk_dims = NN_DIM_NUMBERS if q_layout == HEAD_DIM_MINOR else NT_DIM_NUMBERS
    dk = lax.dot_general(
        ds.astype(do.dtype), q, dk_dims, preferred_element_type=jnp.float32
    )
    dk = dk.astype(dk_scratch_ref.dtype) + dk_scratch_ref[slice_k, :]
    dk_scratch_ref[slice_k, :] = dk
    if dq_scratch_ref is not None or dq_ref is not None:
      dq = lax.dot_general(
          ds.T.astype(k.dtype), k, NN_DIM_NUMBERS,
          preferred_element_type=jnp.float32,
      )
      if dq_scratch_ref is not None:
        # Compute block size != memory block size
        dq_scratch_ref[...] += dq
      else:
        # Compute block size == memory block size
        assert dq_ref is not None
        dq_ref[...] = dq.astype(dq_ref.dtype)

  if dq_scratch_ref is not None:
    dq_scratch_ref[...] = jnp.zeros_like(dq_scratch_ref)
  elif dq_scratch_ref is None and dq_ref is not None:
    dq_ref[...] = jnp.zeros_like(dq_ref)

  @pl.when(should_run)
  def run():
    num_iters = (
        k_ref.shape[0 if k_layout is HEAD_DIM_MINOR else 1] // bkv_compute
    )
    lax.fori_loop(0, num_iters, body, None, unroll=True)
  if dq_scratch_ref is not None:
    assert dq_ref is not None
    dq_ref[...] = dq_scratch_ref[...].astype(dq_ref.dtype)

  should_write = q_index == grid_width - 1
  if is_mqa:
    should_write = jnp.logical_and(
        should_write, q_head_index == num_q_heads - 1
    )
  elif num_kv_heads < num_q_heads:
    assert q_heads_per_kv_heads is not None
    should_write = jnp.logical_and(
        should_write, q_head_index_per_kv_head == q_heads_per_kv_heads - 1
    )

  @pl.when(should_write)
  def end():
    dk_ref[...] = dk_scratch_ref[...].astype(dk_ref.dtype)
    dv_ref[...] = dv_scratch_ref[...].astype(dv_ref.dtype)
    if dq_scratch_ref is not None:
      dq_scratch_ref[...] = jnp.zeros_like(dq_scratch_ref)

    dk_scratch_ref[...] = jnp.zeros_like(dk_scratch_ref)
    dv_scratch_ref[...] = jnp.zeros_like(dv_scratch_ref)

