
def paged_flash_attention_kernel_inline_seq_dim(
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
):
  core_index, b, h = pl.program_id(0), pl.program_id(1), pl.program_id(2)

  # Initialize the output HBM buffers to avoid accessing garbage memory inside
  # the kernel body below.
  m_ref[...] = jnp.full_like(m_ref, -jnp.inf)
  l_ref[...] = jnp.zeros_like(l_ref)
  o_ref[...] = jnp.zeros_like(o_ref)

  def body(i, _):
    paged_flash_attention_kernel(
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
        batch_size=batch_size,
        pages_per_compute_block=pages_per_compute_block,
        pages_per_sequence=pages_per_sequence,
        mask_value=mask_value,
        attn_logits_soft_cap=attn_logits_soft_cap,
        megacore_mode=megacore_mode,
        program_ids=(core_index, b, h, i),
    )
    return ()

  bk = pages_per_compute_block * k_pages_hbm_ref.shape[-2]

  if megacore_mode == "batch":
    num_cores = pl.num_programs(0)
    length = lengths_ref[b * num_cores + core_index]
  else:
    length = lengths_ref[b]

  lax.fori_loop(0, lax.div(length + bk - 1, bk), body, ())

