
def ragged_paged_attention_kernel(
    # Prefetch
    kv_lens_ref,  # [max_num_seqs]
    page_indices_ref,  # [max_num_seqs, pages_per_seq]
    cu_q_lens_ref,  # [max_num_seqs + 1]
    seq_buf_idx_ref,
    # TODO(jevinjiang): if OOM in SMEM, consider pack to other scalar refs.
    num_seqs_ref,
    # Input
    q_ref,  # [num_q_per_blk, num_q_heads_per_blk, head_dim]
    kv_pages_hbm_ref,  # [total_num_pages, page_size, num_combined_kv_heads, head_dim]
    # Output
    o_ref,  # [num_q_per_blk, num_q_heads_per_blk, head_dim]
    # Scratch
    kv_bufs,  # [2, num_kv_pages_per_blk, page_size, num_combined_kv_heads_per_blk, head_dim]
    sems,  # [2, 2]
    l_ref,  # [num_kv_heads_per_blk, num_q_per_blk * num_q_heads_per_kv_head, 128]
    m_ref,  # [num_kv_heads_per_blk, num_q_per_blk * num_q_heads_per_kv_head, 128]
    acc_ref,  # [num_q_per_blk, num_q_heads_per_blk, head_dim]
    *,
    sm_scale: float,
    sliding_window: int | None = None,
    soft_cap: float | None = None,
    mask_value: float | None = DEFAULT_MASK_VALUE,
    k_scale: float | None = None,
    v_scale: float | None = None,
):
  if mask_value is None:
    mask_value = DEFAULT_MASK_VALUE
  num_q_per_blk, num_q_heads_per_blk, head_dim = q_ref.shape
  pages_per_seq = page_indices_ref.shape[-1]
  num_seqs = num_seqs_ref[0]
  _, num_kv_pages_per_blk, page_size, num_combined_kv_heads_per_blk, _ = (
      kv_bufs.shape
  )
  num_kv_heads_per_blk = num_combined_kv_heads_per_blk // 2
  num_kv_per_blk = num_kv_pages_per_blk * page_size
  num_q_heads_per_kv_head = num_q_heads_per_blk // num_kv_heads_per_blk
  heads_blk_idx, q_blk_idx = (
      pl.program_id(0),
      pl.program_id(1),
  )
  num_heads_blks = pl.num_programs(0)
  init_seq_idx = seq_buf_idx_ref[0]
  init_buf_idx = seq_buf_idx_ref[1]
  q_len_start = q_blk_idx * num_q_per_blk
  q_len_end = q_len_start + num_q_per_blk

  def create_kv_async_copy_descriptors(
      heads_blk_idx, seq_idx, kv_blk_idx, buf_idx
  ):
    start_kv_page_idx = kv_blk_idx * num_kv_pages_per_blk
    end_kv_page_idx = jnp.minimum(
        pages_per_seq, pl.cdiv(kv_lens_ref[seq_idx], page_size)
    )
    metadata = (seq_idx, start_kv_page_idx, end_kv_page_idx)
    heads_start = heads_blk_idx * num_combined_kv_heads_per_blk
    async_copy_kv = MultiPageAsyncCopyDescriptor(
        kv_pages_hbm_ref.at[
            :, :, pl.ds(heads_start, num_combined_kv_heads_per_blk), :
        ],
        kv_bufs.at[buf_idx],
        sems.at[buf_idx],
        page_indices_ref,
        metadata,
    )
    return async_copy_kv

  # TODO(jevinjiang): Add these to Mosaic:
  # 1. Support arbitrary strided load/store for int4 and int8 dtype.
  # 2. Support arbitrary strided load/store for any last dimension.
  def strided_load_kv(ref, start, step):
    packing = get_dtype_packing(ref.dtype)
    if packing == 1:
      return [ref[start::step, :]], [ref[start + 1 :: step, :]]
    assert packing in (2, 4, 8)
    assert step % packing == 0
    k_list, v_list = [], []
    b_start = start // packing
    b_step = step // packing
    b_ref = ref.bitcast(jnp.uint32)
    b = b_ref[b_start::b_step, :]

    # TODO(chengjiyao): use the general strided loading logic for bf16 after
    # fixing the issue in mosaic's infer vector layout pass
    if ref.dtype == jnp.bfloat16:
      bk = b << 16
      bv = b & jnp.uint32(0xFFFF0000)
      k = pltpu.bitcast(bk, jnp.float32).astype(jnp.bfloat16)
      v = pltpu.bitcast(bv, jnp.float32).astype(jnp.bfloat16)
      k_list.append(k)
      v_list.append(v)
    else:
      bitwidth = 32 // packing
      bitcast_dst_dtype = jnp.dtype(f"uint{bitwidth}")
      for i in range(0, packing, 2):
        bk = b >> (i * bitwidth)
        k = pltpu.bitcast(bk.astype(bitcast_dst_dtype), ref.dtype)
        k_list.append(k)
        bv = b >> ((i + 1) * bitwidth)
        v = pltpu.bitcast(bv.astype(bitcast_dst_dtype), ref.dtype)
        v_list.append(v)

    return k_list, v_list

  def fold_on_2nd_minor(vec):
    assert vec.dtype == jnp.bfloat16 or vec.dtype == jnp.float32
    assert len(vec.shape) >= 2
    last_dim = vec.shape[-1]
    packing = get_dtype_packing(vec.dtype)
    if vec.shape[-2] % packing != 0:
      vec = vec.astype(jnp.float32)
    return vec.reshape(-1, last_dim)

  @pl.when(heads_blk_idx + q_blk_idx == 0)
  def prefetch_first_kv_blk():
    async_copy_kv = create_kv_async_copy_descriptors(
        heads_blk_idx, init_seq_idx, 0, init_buf_idx
    )
    async_copy_kv.start()

  def is_cur_q_blk_needed(q_states):
    done, cur_seq_idx, _ = q_states
    should_run = jnp.logical_and(q_len_start < cu_q_lens_ref[num_seqs],
                                 cur_seq_idx < num_seqs)
    return jnp.logical_and(done == 0, should_run)

  def compute_with_cur_q_blk(q_states):
    done, cur_seq_idx, cur_buf_idx = q_states
    q_start = cu_q_lens_ref[cur_seq_idx]
    q_end = cu_q_lens_ref[cur_seq_idx + 1]
    q_len = q_end - q_start
    kv_len = kv_lens_ref[cur_seq_idx]

    def get_next_prefetch_ids(
        heads_blk_idx, cur_seq_idx, kv_blk_idx, cur_buf_idx
    ):
      next_kv_blk_idx = kv_blk_idx + 1
      is_last_kv_blk = next_kv_blk_idx * num_kv_per_blk >= kv_len
      next_kv_blk_idx = lax.select(
          is_last_kv_blk,
          0,
          next_kv_blk_idx,
      )
      is_cur_seq_end_in_cur_q_blk = q_end <= q_len_end
      next_seq_idx = lax.select(
          is_last_kv_blk,
          lax.select(is_cur_seq_end_in_cur_q_blk, cur_seq_idx + 1, cur_seq_idx),
          cur_seq_idx,
      )
      is_last_seq = next_seq_idx == num_seqs
      next_seq_idx = lax.select(
          is_last_seq,
          0,
          next_seq_idx,
      )
      next_heads_blk_idx = lax.select(
          is_last_seq,
          heads_blk_idx + 1,
          heads_blk_idx,
      )
      next_buf_idx = lax.select(cur_buf_idx == 0, 1, 0)
      return next_heads_blk_idx, next_seq_idx, next_kv_blk_idx, next_buf_idx

    def flash_attention(
        q,  # [num_q_per_blk * num_q_heads_per_kv_head, head_dim]
        k,  # [num_kv_per_blk, head_dim]
        v,  # [num_kv_per_blk, head_dim]
        head_l_ref,  # [num_q_per_blk * num_q_heads_per_kv_head, 128]
        head_m_ref,  # [num_q_per_blk * num_q_heads_per_kv_head, 128]
        head_acc_ref,  # [num_q_per_blk, num_q_heads_per_kv_head, head_dim]
        *,
        kv_blk_idx,
    ):
      assert q.shape == (
          num_q_per_blk * num_q_heads_per_kv_head,
          head_dim,
      )
      assert (
          k.shape
          == v.shape
          == (
              num_kv_per_blk,
              head_dim,
          )
      )
      assert k.dtype == v.dtype
      assert (
          head_m_ref.shape
          == head_l_ref.shape
          == (
              num_q_per_blk * num_q_heads_per_kv_head,
              128,
          )
      )
      assert head_acc_ref.shape == (
          num_q_per_blk,
          num_q_heads_per_kv_head,
          head_dim,
      )
      kv_len_start = kv_blk_idx * num_kv_per_blk

      def masked_store(ref, val, start, end, group=1):
        iota = lax.broadcasted_iota(jnp.int32, ref.shape, 0) // group
        pltpu.store(ref, val, mask=jnp.logical_and(iota >= start, iota < end))

      def load_with_init(ref, init_val):
        return jnp.where(
            kv_blk_idx == 0, jnp.full_like(ref, init_val), ref[...]
        )

      # kv lens will be contracting dim, we should mask out the NaNs.
      kv_mask = (
          lax.broadcasted_iota(jnp.int32, k.shape, 0) < kv_len - kv_len_start
      )
      k = jnp.where(kv_mask, k.astype(jnp.float32), 0).astype(k.dtype)
      v = jnp.where(kv_mask, v.astype(jnp.float32), 0).astype(v.dtype)

      qk = (
          jnp.einsum("nd,md->nm", q, k, preferred_element_type=jnp.float32)
          * sm_scale
      )
      store_start = jnp.maximum(q_start - q_len_start, 0)
      store_end = jnp.minimum(q_end - q_len_start, num_q_per_blk)

      row_ids = (
          (kv_len - q_len)
          + q_len_start
          - q_start
          + jax.lax.broadcasted_iota(
              jnp.int32,
              (num_q_per_blk * num_q_heads_per_kv_head, num_kv_per_blk),
              0,
          )
          // num_q_heads_per_kv_head
      )
      col_ids = kv_len_start + jax.lax.broadcasted_iota(
          jnp.int32,
          (num_q_per_blk * num_q_heads_per_kv_head, num_kv_per_blk),
          1,
      )
      causal_mask = row_ids < col_ids
      if sliding_window is not None:
        causal_mask = jnp.logical_or(causal_mask,
                                     row_ids - sliding_window >= col_ids)
      if soft_cap is not None:
        qk = soft_cap * jnp.tanh(qk / soft_cap)
      qk += jnp.where(causal_mask, mask_value, 0.0)
      m_curr = jnp.max(qk, axis=1, keepdims=True)
      s_curr = jnp.exp(qk - m_curr)
      qkv = jnp.dot(s_curr, v, preferred_element_type=jnp.float32)
      lm_store_shape = head_m_ref.shape
      m_curr = jnp.broadcast_to(m_curr, lm_store_shape)
      l_curr = jnp.broadcast_to(
          s_curr.sum(axis=1, keepdims=True), lm_store_shape
      )
      m_prev = load_with_init(head_m_ref, -jnp.inf)
      l_prev = load_with_init(head_l_ref, 0.0)
      m_next = jnp.maximum(m_prev, m_curr)
      masked_store(
          head_m_ref, m_next, store_start, store_end, num_q_heads_per_kv_head
      )
      alpha = jnp.exp(m_prev - m_next)
      beta = jnp.exp(m_curr - m_next)
      l_alpha = alpha * l_prev
      l_next = l_alpha + beta * l_curr
      l_next_safe = jnp.where(l_next == 0.0, 1.0, l_next)
      masked_store(
          head_l_ref,
          l_next_safe,
          store_start,
          store_end,
          num_q_heads_per_kv_head,
      )

      def broadcast_to_shape(arr, shape):
        if arr.shape == shape:
          return arr
        assert len(arr.shape) == len(shape)
        assert arr.shape[0] == shape[0]
        assert shape[1] % arr.shape[1] == 0
        # no-op concatenation.
        return jnp.concatenate(
            [arr for _ in range(shape[1] // arr.shape[1])], axis=1
        )

      o_curr = load_with_init(head_acc_ref, 0.0).reshape(-1, head_dim)
      l_alpha = broadcast_to_shape(l_alpha, qkv.shape)
      beta = broadcast_to_shape(beta, qkv.shape)
      l_next_safe = broadcast_to_shape(l_next_safe, qkv.shape)
      out = lax.div(
          l_alpha * o_curr + beta * qkv,
          l_next_safe,
      )
      masked_store(
          head_acc_ref,
          out.reshape(head_acc_ref.shape),
          store_start,
          store_end,
      )

    def is_valid_kv_blk_in_cur_seq(kv_states):
      kv_blk_idx, _ = kv_states
      return kv_blk_idx * num_kv_per_blk < kv_len

    def compute_with_kv_blk_in_cur_seq(kv_states):
      kv_blk_idx, cur_buf_idx = kv_states
      next_heads_blk_idx, next_seq_idx, next_kv_blk_idx, next_buf_idx = (
          get_next_prefetch_ids(
              heads_blk_idx, cur_seq_idx, kv_blk_idx, cur_buf_idx
          )
      )

      @pl.when(next_heads_blk_idx < num_heads_blks)
      def prefetch_next_kv_blk():
        # TODO(jevinjiang): reuse the same buffer if it is already prefetched!
        # TODO(jevinjiang): only fetch effective dynamic size to hold kv_len and
        # DMA to fixed size buffer!
        next_async_copy_kv = create_kv_async_copy_descriptors(
            next_heads_blk_idx, next_seq_idx, next_kv_blk_idx, next_buf_idx
        )
        next_async_copy_kv.start()

      cur_async_copy_kv = create_kv_async_copy_descriptors(
          heads_blk_idx, cur_seq_idx, kv_blk_idx, cur_buf_idx
      )
      kv_ref = cur_async_copy_kv.wait().reshape(
          num_kv_pages_per_blk * page_size * num_combined_kv_heads_per_blk,
          head_dim,
      )
      kv_packing = get_dtype_packing(kv_ref.dtype)
      # NOTE: kv_packing is divided by 2 because k and v are packed together.
      kv_load_step = max(1, kv_packing // 2)
      for kv_head_chunk_idx in range(0, num_kv_heads_per_blk, kv_load_step):
        k_list, v_list = strided_load_kv(
            kv_ref, kv_head_chunk_idx * 2, num_combined_kv_heads_per_blk
        )
        for step_idx in range(kv_load_step):
          k = k_list[step_idx]
          v = v_list[step_idx]
          if k_scale is not None:
            # NOTE: Conversion between arbitrary data types is not supported.
            # That's why it is converted to float32 first.
            k = k.astype(jnp.float32) * k_scale
            k = k.astype(q_ref.dtype)
          if v_scale is not None:
            v = v.astype(jnp.float32) * v_scale
            v = v.astype(q_ref.dtype)
          kv_head_idx = kv_head_chunk_idx + step_idx
          q_head_idx = kv_head_idx * num_q_heads_per_kv_head
          # TODO(jevinjiang): extra handling for packed type that can start at
          # unaligned position!
          q = fold_on_2nd_minor(
              q_ref[:, q_head_idx : q_head_idx + num_q_heads_per_kv_head, :]
          )
          flash_attention(
              q,
              k,
              v,
              l_ref.at[kv_head_idx],
              m_ref.at[kv_head_idx],
              acc_ref.at[
                  :, q_head_idx : q_head_idx + num_q_heads_per_kv_head, :
              ],
              kv_blk_idx=kv_blk_idx,
          )
      return kv_blk_idx + 1, next_buf_idx

    _, next_buf_idx = lax.while_loop(
        is_valid_kv_blk_in_cur_seq,
        compute_with_kv_blk_in_cur_seq,
        (0, cur_buf_idx),  # (kv_blk_idx, buf_idx)
    )
    next_seq_idx = lax.select(q_end <= q_len_end, cur_seq_idx + 1, cur_seq_idx)
    done = lax.select(q_end < q_len_end, done, 1)
    return done, next_seq_idx, next_buf_idx

  _, seq_idx, buf_idx = lax.while_loop(
      is_cur_q_blk_needed,
      compute_with_cur_q_blk,
      (0, init_seq_idx, init_buf_idx),  # (done, seq_idx, buf_idx)
  )
  # Reset seq_idx for next kv_heads_blk if run out of seqs!
  seq_buf_idx_ref[0] = lax.select(seq_idx < num_seqs, seq_idx, 0)
  seq_buf_idx_ref[1] = buf_idx
  o_ref[...] = acc_ref[...].astype(q_ref.dtype)

