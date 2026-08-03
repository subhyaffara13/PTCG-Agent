import functools

def ragged_paged_attention(
    q: jax.Array,  # [max_num_batched_tokens, num_q_heads, head_dim]
    # TODO(jevinjiang): create a write_to_kv_cache kernel!
    kv_pages: jax.Array,  # [total_num_pages, page_size, num_combined_kv_heads, head_dim]
    kv_lens: jax.Array,  # i32[max_num_seqs]
    page_indices: jax.Array,  # i32[max_num_seqs, pages_per_seq]
    cu_q_lens: jax.Array,  # i32[max_num_seqs + 1]
    num_seqs: jax.Array,  # i32[1]
    *,
    sm_scale: float = 1.0,
    sliding_window: int | None = None,
    soft_cap: float | None = None,
    mask_value: float | None = DEFAULT_MASK_VALUE,
    k_scale: float | None = None,
    v_scale: float | None = None,
    num_kv_pages_per_block: int | None = None,
    num_queries_per_block: int | None = None,
    vmem_limit_bytes: int | None = None,
):
  """Ragged paged attention that supports mixed prefill and decode.

  Args:
    q: concatenated all sequences' queries.
    kv_pages: paged KV cache. Normally in HBM.
    kv_lens: padded kv lengths. Only the first num_seqs values are valid.
    page_indices: the first index indicates which page to use in the kv cache
      for each sequence. Only the first num_seqs values are valid.
    cu_q_lens: the cumulative sum of the effective query lengths. Similar to
      kv_lens, only the first num_seqs+1 values are valid.
    num_seqs: the dynamic number of sequences.
    sm_scale: the softmax scale which will be applied to the Q@K^T.
    sliding_window: the sliding window size for the attention.
    soft_cap: the logit soft cap for the attention.
    mask_value: mask value for causal mask.
    k_scale: the scale for the key cache.
    v_scale: the scale for the value cache.
    num_kv_pages_per_block: number of kv pages to be processed in one flash
      attention block in the pallas kernel.
    num_queries_per_block: number of kv pages to be processed in one flash
      attention block in the pallas kernel.
    vmem_limit_bytes: the vmem limit for the pallas kernel.

  Returns:
    The output of the attention.
  """
  static_validate_inputs(
      q,
      kv_pages,
      kv_lens,
      page_indices,
      cu_q_lens,
      num_seqs,
      sm_scale=sm_scale,
      sliding_window=sliding_window,
      soft_cap=soft_cap,
      mask_value=mask_value,
      k_scale=k_scale,
      v_scale=v_scale,
      num_kv_pages_per_block=num_kv_pages_per_block,
      num_queries_per_block=num_queries_per_block,
      vmem_limit_bytes=vmem_limit_bytes,
  )
  if mask_value is None:
    mask_value = DEFAULT_MASK_VALUE
  num_q_tokens, num_q_heads, head_dim = q.shape
  _, page_size, num_combined_kv_heads, _ = kv_pages.shape
  assert num_combined_kv_heads % 2 == 0
  num_kv_heads = num_combined_kv_heads // 2
  _, pages_per_seq = page_indices.shape
  num_q_heads_per_blk, num_combined_kv_heads_per_blk = get_min_heads_per_blk(
      num_q_heads, num_combined_kv_heads, q.dtype, kv_pages.dtype
  )
  num_q_per_blk = num_queries_per_block
  num_kv_pages_per_blk = num_kv_pages_per_block
  if num_q_per_blk is None or num_kv_pages_per_blk is None:
    num_kv_pages_per_blk, num_q_per_blk = get_tuned_block_sizes(
        q.dtype,
        kv_pages.dtype,
        num_q_heads_per_blk,
        num_combined_kv_heads_per_blk // 2,
        head_dim,
        page_size,
        num_q_tokens,
        pages_per_seq,
    )
  num_q_heads_per_kv_head = num_q_heads // num_kv_heads
  num_q_blks = pl.cdiv(num_q_tokens, num_q_per_blk)
  assert num_combined_kv_heads_per_blk % 2 == 0
  num_kv_heads_per_blk = num_combined_kv_heads_per_blk // 2
  assert num_q_heads_per_blk % num_q_heads_per_kv_head == 0
  num_heads_blks = num_q_heads // num_q_heads_per_blk
  grid = (num_heads_blks, num_q_blks)

  def q_index_map(heads_blk_idx, q_blk_idx, *_):
    return (q_blk_idx, heads_blk_idx, 0)

  q_block_spec = pl.BlockSpec(
      (num_q_per_blk, num_q_heads_per_blk, head_dim),
      q_index_map,
  )
  in_specs = [
      q_block_spec,
      pl.BlockSpec(memory_space=pl.ANY),
  ]
  out_specs = q_block_spec
  lm_scratch = pltpu.VMEM(
      # TODO(jevinjiang): use 128 instead of 1 is due to Mosaic does not support
      # unaligned slicing!
      (num_kv_heads_per_blk, num_q_per_blk * num_q_heads_per_kv_head, 128),
      jnp.float32,
  )
  acc_scratch = pltpu.VMEM(
      (num_q_per_blk, num_q_heads_per_blk, head_dim),
      jnp.float32,
  )
  double_buf_scratch = pltpu.VMEM(
      (
          2,  # For double buffering during DMA copies.
          num_kv_pages_per_blk,
          page_size,
          num_combined_kv_heads_per_blk,
          head_dim,
      ),
      kv_pages.dtype,
  )
  scratch_shapes = [
      double_buf_scratch,  # kv_bufs
      pltpu.SemaphoreType.DMA((2,)),  # Semaphores for double buffers.
      lm_scratch,  # l_ref
      lm_scratch,  # m_ref
      acc_scratch,
  ]
  scalar_prefetches = (
      kv_lens,
      page_indices,
      cu_q_lens,
      jnp.array((0, 0), jnp.int32),  # seq_idx, buf_idx
      num_seqs,
  )
  kernel = pl.pallas_call(
      functools.partial(
          ragged_paged_attention_kernel,
          sm_scale=sm_scale,
          sliding_window=sliding_window,
          soft_cap=soft_cap,
          mask_value=mask_value,
          k_scale=k_scale,
          v_scale=v_scale,
      ),
      grid_spec=pltpu.PrefetchScalarGridSpec(
          num_scalar_prefetch=len(scalar_prefetches),
          in_specs=in_specs,
          out_specs=out_specs,
          grid=grid,
          scratch_shapes=scratch_shapes,
      ),
      compiler_params=pltpu.CompilerParams(
          dimension_semantics=(
              "arbitrary",
              "arbitrary",
          ),
          vmem_limit_bytes=vmem_limit_bytes,
      ),
      out_shape=jax.ShapeDtypeStruct(shape=q.shape, dtype=q.dtype),
      name="ragged_paged_attention_kernel",
  )

  return kernel(*scalar_prefetches, q, kv_pages)

