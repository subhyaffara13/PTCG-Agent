
def paged_flash_attention_kernel(
    lengths_ref,
    page_indices_ref,
    buffer_index_ref,
    init_flag_ref,
    q_ref,
    k_pages_hbm_ref,
    k_scales_pages_hbm_ref,
    v_pages_hbm_ref,
    v_scales_pages_hbm_ref,
    o_ref,
    m_ref,
    l_ref,
    k_vmem_buffer,
    k_scales_vmem_buffer,
    v_vmem_buffer,
    v_scales_vmem_buffer,
    k_sems,
    v_sems,
    *,
    batch_size: int,
    pages_per_compute_block: int,
    pages_per_sequence: int,
    mask_value: float,
    attn_logits_soft_cap: float | None,
    megacore_mode: str | None,
    program_ids=(),
):
  """Pallas kernel for paged attention."""
  if program_ids:
    core_index, b, h, i = program_ids
  else:
    core_index, b, h, i = (
        pl.program_id(0),
        pl.program_id(1),
        pl.program_id(2),
        pl.program_id(3),
    )
  num_kv_heads, _, page_size, _ = k_pages_hbm_ref.shape
  bk = page_size * pages_per_compute_block
  num_cores = pl.num_programs(0)

  b_step = num_cores if megacore_mode == "batch" else 1
  b_start = core_index if megacore_mode == "batch" else 0
  h_step = num_cores if megacore_mode == "kv_head" else 1
  h_start = core_index if megacore_mode == "kv_head" else 0

  h = h * h_step + h_start
  b = b * b_step + b_start
  length = lengths_ref[b]

  def compute_block_indices(b, h, i):

    def advance_b():
      next_b = b + b_step

      def advance_to_next_non_zero_length():
        next_next_b = next_b + b_step
        return lax.fori_loop(
            lax.div(next_next_b, b_step),
            lax.div(batch_size, b_step),
            lambda _, b: jnp.where(lengths_ref[b] == 0, b + b_step, b),
            next_next_b,
        )

      return (
          lax.cond(
              jnp.logical_and(
                  next_b < batch_size,
                  lengths_ref[lax.clamp(0, next_b, batch_size - 1)] == 0),
              advance_to_next_non_zero_length,
              lambda: next_b,
          ),
          h_start,
          0,
      )

    def advance_h():
      next_h = h + h_step
      return lax.cond(next_h < num_kv_heads, lambda: (b, next_h, 0), advance_b)

    return lax.cond(i * bk < lengths_ref[b], lambda: (b, h, i), advance_h)

  def create_kv_async_copy_descriptors(b, h, i, buffer_index):
    page_offset = b * pages_per_sequence + i * pages_per_compute_block
    pages_to_load = pages_per_compute_block
    async_copy_k = MultiPageAsyncCopyDescriptor(
        k_pages_hbm_ref,
        k_scales_pages_hbm_ref,
        k_vmem_buffer.at[buffer_index],
        k_scales_vmem_buffer.at[buffer_index]
        if k_scales_vmem_buffer is not None
        else None,
        k_sems.at[buffer_index],
        page_indices_ref,
        page_offset,
        pages_to_load,
        h,
    )
    async_copy_v = MultiPageAsyncCopyDescriptor(
        v_pages_hbm_ref,
        v_scales_pages_hbm_ref,
        v_vmem_buffer.at[buffer_index],
        v_scales_vmem_buffer.at[buffer_index]
        if v_scales_vmem_buffer is not None
        else None,
        v_sems.at[buffer_index],
        page_indices_ref,
        page_offset,
        pages_to_load,
        h,
    )
    return async_copy_k, async_copy_v

  @pl.when(i * bk < length)
  def flash_attention():
    init_flag = init_flag_ref[0]
    init_flag_ref[0] = 0
    buffer_index = buffer_index_ref[0]
    next_b, next_h, next_i = compute_block_indices(b, h, i + 1)

    @pl.when(init_flag)
    def prefetch_first_block():
      async_copy_k, async_copy_v = create_kv_async_copy_descriptors(
          b, h, i, buffer_index
      )
      async_copy_k.start()
      async_copy_v.start()

    @pl.when(i == 0)
    def init():
      m_ref[...] = jnp.full_like(m_ref, -jnp.inf)
      l_ref[...] = jnp.zeros_like(l_ref)
      o_ref[...] = jnp.zeros_like(o_ref)

    @pl.when(next_b < batch_size)
    def prefetch_next_block():
      next_buffer_index = jnp.where(buffer_index == 0, 1, 0)
      async_copy_next_k, async_copy_next_v = create_kv_async_copy_descriptors(
          next_b, next_h, next_i, next_buffer_index
      )
      async_copy_next_k.start()
      async_copy_next_v.start()
      buffer_index_ref[0] = next_buffer_index

    async_copy_k, async_copy_v = create_kv_async_copy_descriptors(
        b, h, i, buffer_index
    )
    q = q_ref[...].astype(jnp.float32)
    k = async_copy_k.wait_and_get_loaded()
    qk = jnp.einsum("gd,td->gt", q, k, preferred_element_type=jnp.float32)
    if attn_logits_soft_cap is not None:
      capped_qk = jnp.tanh(qk / attn_logits_soft_cap)
      qk = capped_qk * attn_logits_soft_cap

    mask = i * bk + jax.lax.broadcasted_iota(jnp.int32, qk.shape, 1) < length
    qk = qk + jnp.where(mask, 0.0, mask_value)
    m_curr = qk.max(axis=-1)

    s_curr = jnp.exp(qk - m_curr[..., None])
    m_prev, l_prev = m_ref[...], l_ref[...]
    l_curr = jax.lax.broadcast_in_dim(s_curr.sum(axis=-1), l_prev.shape, (0,))
    m_curr = jax.lax.broadcast_in_dim(m_curr, m_prev.shape, (0,))
    m_next = jnp.maximum(m_prev, m_curr)
    alpha = jnp.exp(m_prev - m_next)
    beta = jnp.exp(m_curr - m_next)
    l_next = alpha * l_prev + beta * l_curr
    m_ref[...], l_ref[...] = m_next, l_next

    v = async_copy_v.wait_and_get_loaded()
    o_curr = jnp.einsum("gt,td->gd", s_curr, v)

    o_ref[...] = (
        (l_prev * alpha * o_ref[...] + beta * o_curr) / l_next
    ).astype(o_ref.dtype)

