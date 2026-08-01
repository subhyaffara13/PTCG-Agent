
def paged_attention_kernel(
    # inputs
    q_ref,  # [block_h, head_dim]
    k_pages_ref,  # [total_num_pages, page_size, head_dim]
    k_scales_pages_ref,  # [total_num_pages, page_size]
    v_pages_ref,  # [total_num_pages, page_size, head_dim]
    v_scales_pages_ref,  # [total_num_pages, page_size]
    block_tables_ref,  # [pages_per_partition]
    lengths_ref,  # [1]
    # outputs
    o_ref: Any,  # [block_h, head_dim]
    *residual_refs: Any,  # Residual outputs: [block_h,], [block_h,]
    num_heads: int,
    pages_per_compute_block: int,
    mask_value: float,
    attn_logits_soft_cap: float | None,
):
  partition_idx = pl.program_id(2)
  block_h, head_dim = q_ref.shape
  page_size = k_pages_ref.shape[-2]
  pages_per_partition = block_tables_ref.shape[0]
  block_k = pages_per_compute_block * page_size

  def _compute(start_page_idx, end_page_idx, o, m_i, l_i):
    q_slice = pl.ds(0, block_h)
    q = q_ref[q_slice, :]

    # Loop over blocks of pages to process a entire page sequence partition.
    # Grid loops over q blocks over num_heads.
    def body(start_k, carry):
      o_prev, m_prev, l_prev = carry

      block_tables_slice = pl.ds(
          start_k * pages_per_compute_block, pages_per_compute_block
      )
      block_tables = block_tables_ref[block_tables_slice]
      k = k_pages_ref[block_tables].reshape(block_k, head_dim)
      v = v_pages_ref[block_tables].reshape(block_k, head_dim)
      if k_scales_pages_ref is not None:
        # dynamic lhs quantized dot is not currently implemented
        # so we cast rhs to the lhs dtype
        k = k.astype(q.dtype)
      uncapped_logits = plgpu.dot(q, k.T)  # [block_h, block_k]
      if k_scales_pages_ref is not None:
        # k_scales_pages_ref are one per head
        # they're laid out across the output dimension, so scale output
        k_scale = k_scales_pages_ref[block_tables].reshape((1, block_k))
        uncapped_logits *= k_scale.astype(uncapped_logits.dtype)
      if attn_logits_soft_cap is not None:
        logits = jnp.tanh(uncapped_logits / attn_logits_soft_cap)
        logits = logits * attn_logits_soft_cap
      else:
        logits = uncapped_logits

      if lengths_ref is not None:
        curr_start_page_idx = (
            partition_idx * pages_per_partition
            + start_k * pages_per_compute_block
        )
        curr_start_token_idx = curr_start_page_idx * page_size

        mask = jnp.arange(block_k) + curr_start_token_idx < lengths_ref[0]
        mask = lax.broadcast_in_dim(mask, (block_h, block_k), (1,))
        logits = jnp.where(mask, logits, mask_value)

      log2e = math.log2(math.e)
      m_curr = logits.max(axis=-1)
      m_next = jnp.maximum(m_prev, m_curr)
      correction = jnp.exp2((m_prev - m_next) * log2e)
      l_prev_corr = correction * l_prev
      s_curr = jnp.exp2((logits - m_next[:, None]) * log2e)
      l_curr = s_curr.sum(axis=-1)
      l_next = l_prev_corr + l_curr
      o_prev_corr = correction[:, None] * o_prev
      if v_scales_pages_ref is not None:
        # v_scales are 1 per head
        # they're laid out across the reduction dimension, so scale lhs
        v_scale = v_scales_pages_ref[block_tables].reshape((1, block_k))
        s_curr *= v_scale.astype(s_curr.dtype)
        # dynamic lhs quantized dot is not currently implemented
        # so we cast rhs to the lhs dtype
        v = v.astype(s_curr.dtype)
      o_curr = plgpu.dot(s_curr.astype(v.dtype), v)

      o_next = o_prev_corr + o_curr
      return o_next, m_next, l_next

    max_it = pl.cdiv(end_page_idx - start_page_idx, pages_per_compute_block)
    (o, m_i, l_i) = lax.fori_loop(0, max_it, body, (o, m_i, l_i))

    return o, m_i, l_i

  m_i = jnp.zeros(block_h, dtype=jnp.float32) + jnp.finfo(jnp.float32).min
  l_i = jnp.zeros(block_h, dtype=jnp.float32)
  o = jnp.zeros((block_h, head_dim), dtype=jnp.float32)

  start_page_idx = partition_idx * pages_per_partition
  end_page_idx = start_page_idx + pages_per_partition

  if lengths_ref is None:
    o, m_i, l_i = _compute(start_page_idx, end_page_idx, o, m_i, l_i)
  else:
    end_page_idx = jnp.minimum(pl.cdiv(lengths_ref[0], page_size), end_page_idx)

    o, m_i, l_i = jax.lax.cond(
        start_page_idx >= end_page_idx,
        lambda: (o, m_i, l_i),
        lambda: _compute(start_page_idx, end_page_idx, o, m_i, l_i),
    )

  o_ref[...] = o.astype(o_ref.dtype)

  if residual_refs is not None:
    l_ref, m_ref = residual_refs
    l_ref[...] = l_i
    m_ref[...] = m_i

