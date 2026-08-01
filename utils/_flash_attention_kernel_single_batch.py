
def _flash_attention_kernel_single_batch(
    batch_idx: tuple[int, ...],
    q_tile_ref,
    k_tile_ref,
    v_tile_ref,
    ab_tile_ref,
    q_segment_ids_tile_ref,
    kv_segment_ids_tile_ref,  # Input arrays
    o_tile_ref,  # Output arrays
    l_ref,
    m_ref,
    m_scratch_ref,
    l_scratch_ref,
    acc_scratch_ref,
    *,
    causal,
    sm_scale,
    block_k,
    kv_seq_len,
    mask_value,
):
  block_k_major = k_tile_ref.shape[2]
  block_q = q_tile_ref.shape[2]
  head_dim = q_tile_ref.shape[-1]

  kv_seq_idx = pl.program_id(3)
  @pl.when(kv_seq_idx == 0)
  def start_new_sequence():
    m_scratch_ref[batch_idx] = jnp.full(
        m_scratch_ref.shape[2:], -jnp.inf, jnp.float32
    )
    l_scratch_ref[batch_idx] = jnp.zeros(l_scratch_ref.shape[2:], jnp.float32)
    acc_scratch_ref[batch_idx] = jnp.zeros(
        acc_scratch_ref.shape[2:], jnp.float32
    )

  q_seq_idx = pl.program_id(2)
  if causal:
    should_run = below_or_on_diag(q_seq_idx, block_q, kv_seq_idx, block_k_major)
  else:
    should_run = True

  @pl.when(should_run)
  def run():
    @pl.loop(0, block_k_major, step=block_k, unroll=True)
    def _body(start_k):
      m_prev = m_scratch_ref[batch_idx]
      l_prev = l_scratch_ref[batch_idx]
      q = q_tile_ref[batch_idx]  # [block_q, head_dim]
      k = k_tile_ref[
          (*batch_idx, pl.dslice(start_k, block_k), slice(None))
      ]  # [block_k, head_dim]

      s = jax.lax.dot_general(
          q, k, TRANS_B_DIM_NUMBERS, preferred_element_type=jnp.float32
      )  # [block_q, block_k]

      # Add attention bias if needed.
      # TODO(tanburn) Should the attention bias be added before or after
      # multiplication by sm_scale?
      if ab_tile_ref is not None:
        ab = ab_tile_ref[
            (*batch_idx, pl.dslice(None), pl.dslice(start_k, block_k))
        ].astype(jnp.float32)
        s += ab

      if sm_scale != 1.0:
        s *= sm_scale

      mask = None
      if q_segment_ids_tile_ref is not None:
        repeats, rem = divmod(block_k, NUM_LANES)
        if rem:
          raise NotImplementedError(
              f"kv block size must be a multiple of {NUM_LANES}"
          )
        q_segment_ids = jnp.tile(
            q_segment_ids_tile_ref[batch_idx[0]], (1, repeats)
        )  # [block_q, block_k].
        kv_segment_ids = kv_segment_ids_tile_ref[
            batch_idx[0], :1, pl.dslice(start_k, block_k)
        ]  # [1, block_k].
        mask = jnp.equal(q_segment_ids, kv_segment_ids).astype(jnp.bool_)

      if causal:
        mask_shape = (block_q, block_k)
        row_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 0)
        row_ids += q_seq_idx * block_q
        col_ids = jax.lax.broadcasted_iota(jnp.int32, mask_shape, 1)
        col_ids += kv_seq_idx * block_k_major + start_k
        causal_mask = col_ids <= row_ids
        mask = (
            causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
        )

      s = s if mask is None else s + jnp.where(mask, 0.0, mask_value)

      m_curr = jnp.max(s, axis=1)[:, None]  # Row max, shape [block_q, 1].
      m_next = jnp.maximum(m_prev, m_curr)  # Shape [block_q, 128].

      block_k_repeats, rem = divmod(block_k, MIN_BLOCK_SIZE)
      if rem:
        raise NotImplementedError(
            f"{block_k=} should be a multiple of {MIN_BLOCK_SIZE}"
        )
      p = jnp.exp(s - jnp.tile(m_next, (1, block_k_repeats)))

      alpha = jnp.exp(m_prev - m_next)  # Shape [block_q, 128].

      l_corr = alpha * l_prev

      l_next = jnp.sum(p, axis=1)[:, None] + l_corr  # Shape [block_q, 128]

      head_dim_repeats, rem = divmod(head_dim, MIN_BLOCK_SIZE)
      l_broadcast = lambda l: jnp.tile(l, (1, head_dim_repeats))
      if rem:
        if head_dim_repeats == 0:
          l_broadcast = lambda l: l[:, :head_dim]
        else:
          raise NotImplementedError(
              f"{head_dim=} should be a multiple of {MIN_BLOCK_SIZE} if larger"
          )
      l_scratch_ref[batch_idx] = l_next
      m_scratch_ref[batch_idx] = m_next

      l_next_inv_safe = jnp.where(l_next == 0.0, 1.0, 1.0 / l_next)
      acc_scratch_ref[batch_idx] *= l_broadcast(l_corr * l_next_inv_safe)
      v = v_tile_ref[(*batch_idx, pl.dslice(start_k, block_k), slice(None))]
      o_curr = jax.lax.dot(
          p.astype(v.dtype), v, preferred_element_type=jnp.float32
      )
      acc_scratch_ref[batch_idx] += o_curr * l_broadcast(l_next_inv_safe)

  @pl.when(kv_seq_idx == (kv_seq_len // block_k_major) - 1)
  def store_output():
    o_tile_ref[batch_idx] = acc_scratch_ref[batch_idx].astype(o_tile_ref.dtype)
    if l_ref is not None:
      l_ref[batch_idx] = l_scratch_ref[batch_idx].astype(l_ref.dtype)
    if m_ref is not None:
      m_ref[batch_idx] = m_scratch_ref[batch_idx].astype(m_ref.dtype)

