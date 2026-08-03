import functools

def flash_attention_kernel(
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
    mask_ref,
    q_sequence_ref,
    # Outputs
    m_scratch_ref,
    l_scratch_ref,
    o_scratch_ref,
    o_ref,
    logsumexp_ref=None,
    *,
    mask_value: float,
    grid_width: int,
    bq: int,
    bkv: int,
    bkv_compute: int,
    head_dim_v: int,
    q_layout: QKVLayout,
    k_layout: QKVLayout,
    v_layout: QKVLayout,
    attn_logits_soft_cap: float | None,
    mask_function: MaskFunctionType | None,
):
  float32 = jnp.float32
  HEAD_DIM_MINOR = QKVLayout.HEAD_DIM_MINOR
  head_dim_v_repeats = pl.cdiv(head_dim_v, NUM_LANES)

  h, i, j = pl.program_id(0), pl.program_id(1), pl.program_id(2)

  @pl.when(j == 0)
  def init():
    o_scratch_ref[...] = jnp.zeros_like(o_scratch_ref)
    if sinks_ref is not None:
      sinks = sinks_ref[0, h].astype(m_scratch_ref.dtype)
      # initialize `max = sinks`, so `exp(sinks - max = 0) = 1`
      m_scratch_ref[...] = sinks * jnp.ones_like(m_scratch_ref)
      l_scratch_ref[...] = jnp.ones_like(l_scratch_ref)
    else:
      m_scratch_ref[...] = jnp.full_like(m_scratch_ref, mask_value)
      l_scratch_ref[...] = jnp.zeros_like(l_scratch_ref)

  global_kv_index, _, should_run, should_not_mask = _next_nonzero(
      h,
      i,
      j,
      data_next_ref,
      block_mask_ref,
      mask_next_ref,
  )

  def body(kv_compute_index, _):
    slice_k = pl.ds(kv_compute_index * bkv_compute, bkv_compute)
    m_prev, l_prev = m_scratch_ref[...], l_scratch_ref[...]
    assert m_prev.shape == (bq, NUM_LANES)
    assert l_prev.shape == (bq, NUM_LANES)

    q = q_ref[...] if q_layout == HEAD_DIM_MINOR else q_ref[...].T
    qk_dims = NT_DIM_NUMBERS if k_layout == HEAD_DIM_MINOR else NN_DIM_NUMBERS
    if k_layout == HEAD_DIM_MINOR:
      k = k_ref[slice_k, :]
    else:
      k = k_ref[:, slice_k]
    qk = lax.dot_general(q, k, qk_dims, preferred_element_type=float32)

    assert qk.shape == (bq, bkv_compute)
    assert isinstance(slice_k, pl.Slice)
    apply_mask_and_soft_cap = functools.partial(
        _apply_mask_and_soft_cap,
        qk,
        mask_value,
        should_not_mask,
        mask_ref,
        q_sequence_ref,
        q_segment_ids_ref,
        kv_segment_ids_ref,
        attn_logits_soft_cap=attn_logits_soft_cap,
        k_slice=slice_k,
        # When the iteration space is shrunk (for local attention for example),
        # the kv_index program_id does not correspond to the actual coordinates
        # of the KV data. Make sure to use the 'unshrunk' index (coming from the
        # data_next array) when computing the mask.
        k_offset=global_kv_index * bkv + kv_compute_index * bkv_compute,
        bq=bq,
        mask_function=mask_function,
    )

    qk = apply_mask_and_soft_cap()
    assert not isinstance(qk, tuple)

    m_curr = qk.max(axis=-1)[:, None]
    assert m_curr.shape == (bq, 1)
    m_next = jnp.maximum(m_prev, m_curr)
    assert m_next.shape == (bq, NUM_LANES)

    bkv_repeats, rem = divmod(bkv_compute, NUM_LANES)
    if rem != 0:
      raise NotImplementedError(
          f"{bkv_compute=} should be a multiple of {NUM_LANES}"
      )

    s_curr = jnp.exp(qk - jnp.tile(m_next, (1, bkv_repeats)))
    assert s_curr.shape == (bq, bkv_compute)

    l_curr = jax.lax.broadcast_in_dim(s_curr.sum(axis=-1), l_prev.shape, (0,))
    assert l_curr.shape == (bq, NUM_LANES)

    alpha = jnp.exp(m_prev - m_next)
    l_next = l_curr + alpha * l_prev
    m_scratch_ref[...], l_scratch_ref[...] = m_next, l_next

    sv_dims = NN_DIM_NUMBERS if v_layout == HEAD_DIM_MINOR else NT_DIM_NUMBERS
    if v_layout == HEAD_DIM_MINOR:
      v = v_ref[slice_k, :]
    else:
      v = v_ref[:, slice_k]
    v = v.astype(float32)
    o_curr = lax.dot_general(s_curr, v, sv_dims)

    alpha_o = jnp.tile(
        alpha, (1, head_dim_v_repeats))[..., :o_scratch_ref.shape[-1]]
    o_scratch_ref[:] = alpha_o * o_scratch_ref[:] + o_curr

  @pl.when(should_run)
  def run():
    assert bkv % bkv_compute == 0
    num_iters = (
        k_ref.shape[0 if k_layout == HEAD_DIM_MINOR else 1] // bkv_compute
    )
    lax.fori_loop(0, num_iters, body, None, unroll=True)

  @pl.when(j == grid_width - 1)
  def end():
    l = l_scratch_ref[...]
    l_inv = jnp.tile(
        1.0 / l, (1, head_dim_v_repeats))[..., :o_scratch_ref.shape[-1]]
    o_ref[...] = (o_scratch_ref[...] * l_inv).astype(o_ref.dtype)
    if logsumexp_ref is not None:
      assert logsumexp_ref.shape == (bq, NUM_LANES)
      logsumexp_ref[...] = (jnp.log(l) + m_scratch_ref[...]).astype(
          logsumexp_ref.dtype
      )

    m_scratch_ref[...] = jnp.zeros_like(m_scratch_ref)
    l_scratch_ref[...] = jnp.zeros_like(l_scratch_ref)
    o_scratch_ref[...] = jnp.zeros_like(o_scratch_ref)

