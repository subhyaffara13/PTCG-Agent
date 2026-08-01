
def paged_attention(
    query: Array,
    key: Array,
    value: Array,
    q_seqlen: Array,
    kv_seqlen: Array,
    page_table_k: Array,
    page_table_v: Array,
    bias: Array | None = None,
    mask: Array | None = None,
    fp8_params: FP8Params | None = None,
    *,
    scale: float = 1.0,
    mask_type: MaskType = MaskType.NO_MASK,
    seed: int = 42,
    dropout_rate: float = 0.,
    qkv_layout: str = "BTNH",
    sliding_window_length: int | None = None,
    use_fp8: bool = False,
    return_residual: bool = False
):
  """Computes paged attention described in https://arxiv.org/pdf/2309.06180.

    B = batch size
    S = length of the key/value (source)
    T = length of the query (target)
    N = number of attention heads
    H = dimensions of each attention head.

  Args:
    query: Queries for attention calculation with a shape of BTNH or BNTH.
    key: Keys for attention calculation with a shape of
      [num_blocks, block_size, N, H] or [num_blocks, N, block_size, H] where
      num_blocks = B * Ceil(S / block_size).
    value: Values to be used in attention with a shape of
      [num_blocks, block_size, N, H] or [num_blocks, N, block_size, H] where
      num_blocks = B * Ceil(S / block_size).
    q_seqlen: Non padded sequence length of query with a shape of B.
    kv_seqlen: Non padded sequence length of key and value with a shape of B.
    page_table_k: page table for key of shape [B, 1, num_blocks_per_batch, 1]
      where num_blocks_per_batch = Ceil(S / block_size).
    page_table_v: page table for value of shape [B, 1, num_blocks_per_batch, 1]
      where num_blocks_per_batch = Ceil(S / block_size).
    bias: Bias to be added to logits with a shape of BNTS.
    mask: Mask used to filter out logits with a shape of BNTS.
    scale: Scale for the query.
    qkv_layout: Layout string, with supported formats being BTNH, BNTH, BSNH,
      BNSH.
    sliding_window_length: Window size to make attention only attend to each
      token's left local window (pos - sliding_window_length, pos] where `pos`
      is the index of each token. E.g., if sliding_window_length == 3 and the
      sequence is [0, 1, 2, 3, c, 4, 5], token `c` can attend to [4, 5, c].
    use_fp8: Whether to use FP8 attention mechanism.
    return_residual: Whether to return the logsumexp tensor of shape BTN
      or BNT to users. See section 3.1.1 in the FlashAttention-2 paper:
      https://arxiv.org/pdf/2307.08691 to find the definition of logsumexp.
  Returns:
    output: the same shape as the query.
    residual: the logsumexp tensor if return_residual=True. (non fp8)
  """
  cudnn_version = check_cudnn_version()
  layout = _normalize_layout(qkv_layout)
  if use_fp8:
    raise ValueError("Paged attention doesn't support fp8 for now.")
  if has_padding(mask_type) and (q_seqlen is None or kv_seqlen is None):
    raise ValueError("Require q_seqlen and kv_seqlen to generate padding mask.")
  if sliding_window_length is not None and sliding_window_length <= 0:
    raise ValueError(
      f"Require sliding_window_length > 0, got {sliding_window_length}.")

  bias = combine_bias_and_mask(bias, mask, query.dtype)
  # check if input shape and data type is compatiable
  check_layout(query, key, value, bias, q_seqlen, kv_seqlen, None, None,
    page_table_k, page_table_v, layout)
  has_bias = bias is not None
  has_dbias = has_bias and \
    should_export_dbias(bias.shape, query.shape, layout)
  variadic_args = (has_bias, has_dbias)

  _not_used = jnp.zeros(0, dtype=query.dtype)
  if bias is None:
    bias = _not_used

  output = _dot_product_attention(
      query, key, value, bias, q_seqlen, kv_seqlen, _not_used, _not_used,
      page_table_k, page_table_v, scale, seed, dropout_rate, variadic_args,
      mask_type, layout.value, sliding_window_length, cudnn_version,
      return_residual)
  return output


def paged_attention(
    q: jax.Array,
    k_pages: jax.Array,
    v_pages: jax.Array,
    block_tables: jax.Array,
    lengths: jax.Array | None,
    k_scales_pages: jax.Array | None = None,
    v_scales_pages: jax.Array | None = None,
    *,
    block_h: int = 16,
    pages_per_compute_block: int = 8,
    k_splits: int = 16,
    num_warps: int = 8,
    num_stages: int = 2,
    interpret: bool = False,
    debug: bool = False,
    mask_value: float = DEFAULT_MASK_VALUE,
    attn_logits_soft_cap: float | None = None,
) -> jax.Array:
  """Paged grouped query attention.

  Args:
    q: A [batch_size, num_heads, head_dim] jax.Array.
    k_pages: A [num_kv_heads, total_num_pages, page_size, head_dim] jax.Array.
    v_pages: A [num_kv_heads, total_num_pages, page_size, head_dim] jax.Array.
    block_tables: A i32[batch_size, pages_per_sequence] jax.Array. Each entry
      should be in the range of [0, total_num_pages), indicating where to locate
      the page in `k_pages` or `v_pages`.
    lengths: A i32[batch_size] jax.Array the length of each example.
    k_scales_pages: A [num_kv_heads, total_num_pages, page_size] jax.Array.
    v_scales_pages: A [num_kv_heads, total_num_pages, page_size] jax.Array.
    block_h: int The block size that partitions the number of head groups.
    pages_per_compute_block: int The maximum number of blocks per compute block.
    k_splits: int Number of partitions used to parallelize key-value sequence
      pages processing.
    mask_value: The value used for padding in attention. By default it is a very
      negative floating point number.
    attn_logits_soft_cap: The value used for soft capping the attention logits.

  Returns:
    The output of attention([batch_size, num_heads, head_dim]).
  """
  batch_size, num_heads, head_dim = q.shape
  num_kv_heads, _, _, head_dim_k = k_pages.shape
  batch_size_paged_indices, _ = block_tables.shape

  if k_pages.shape != v_pages.shape:
    raise ValueError(
        f"k_pages and v_pages must have the same shape. Got {k_pages.shape} and"
        f" {v_pages.shape}"
    )
  if num_heads % num_kv_heads != 0:
    raise ValueError(
        "Number of Q heads must be divisible by number of KV heads. Got"
        f" {num_heads} and {num_kv_heads}."
    )
  if head_dim_k != head_dim:
    raise ValueError(
        "head_dim of Q must be the same as that of K/V. Got"
        f" {head_dim} and {head_dim_k}."
    )
  if batch_size_paged_indices != batch_size:
    raise ValueError("`block_tables` and `q` must have the same batch size")
  if lengths is not None:
    if lengths.shape != (batch_size,):
      raise ValueError("`lengths` and `q` must have the same batch size")
    if lengths.dtype != jnp.int32:
      raise ValueError(
          "The dtype of `lengths` must be int32. Got {lengths.dtype}"
      )

  if block_h % 16:
    raise ValueError(f"block_h must divisible by 16, but is {block_h}.")

  impl = functools.partial(
      paged_attention_unbatched,
      block_h=block_h,
      pages_per_compute_block=pages_per_compute_block,
      k_splits=k_splits,
      num_warps=num_warps,
      num_stages=num_stages,
      interpret=interpret,
      debug=debug,
      mask_value=mask_value,
      attn_logits_soft_cap=attn_logits_soft_cap,
  )

  o = jax.vmap(impl, (0, None, None, 0, 0, None, None), 0)(
      q,
      k_pages,
      v_pages,
      block_tables,
      lengths[..., None] if lengths is not None else None,
      k_scales_pages,
      v_scales_pages,
  )

  return o


def paged_attention(
    q: jax.Array,
    k_pages: jax.Array | quantization_utils.QuantizedTensor,
    v_pages: jax.Array | quantization_utils.QuantizedTensor,
    lengths: jax.Array,
    page_indices: jax.Array,
    *,
    mask_value: float = DEFAULT_MASK_VALUE,
    attn_logits_soft_cap: float | None = None,
    pages_per_compute_block: int,
    megacore_mode: str | None = None,
    inline_seq_dim: bool = True,
) -> jax.Array:
  """Paged grouped query attention.

  Args:
    q: A [batch_size, num_q_heads, head_dim] jax.Array.
    k_pages: A [num_kv_heads, total_num_pages, page_size, head_dim] jax.Array.
    v_pages: A [num_kv_heads, total_num_pages, page_size, head_dim] jax.Array.
    lengths: A i32[batch_size] jax.Array the length of each example.
    page_indices: A i32[batch_size, pages_per_sequence] jax.Array. Each entry
      should be in the range of [0, total_num_pages), indicating where to locate
      the page in `k_pages` or `v_pages`.
    mask_value: The value used for padding in attention. By default it is a very
      negative floating point number.
    attn_logits_soft_cap: The value used for soft capping the attention logits.
    pages_per_compute_block: how many pages to be processed in one flash
      attention block in the pallas kernel.
    megacore_mode: if set, enable megacore to parallelize the computation. Must
      be one of ['kv_head', 'batch', None]. Caveat: set this only if megacore is
      enabled, otherwise the kernel may hang. If you are not sure, leave it to
      None.
      * None: disable megacore parallelism.
      * kv_head: megacore parallelism on KV heads; requires number of KV heads
        divisible by 2.
      * batch: megacore parallelism on batch dimension; requires batch divisible
        by 2.
    inline_seq_dim: whether to fuse kernel instances along the sequence dim into
      one kernel.

  Returns:
    The output of attention([batch_size, num_q_heads, head_dim]).
  """
  if isinstance(k_pages, quantization_utils.QuantizedTensor):
    k_pages, k_scales_pages = k_pages.weight, k_pages.scales
    assert isinstance(k_scales_pages, jax.Array)  # For typing.
    k_scales_pages = jnp.broadcast_to(
        k_scales_pages, (*k_scales_pages.shape[:-1], k_pages.shape[-1])
    )
  else:
    k_scales_pages = None
  if isinstance(v_pages, quantization_utils.QuantizedTensor):
    v_pages, v_scales_pages = v_pages.weight, v_pages.scales
    assert isinstance(v_scales_pages, jax.Array)  # For typing.
    v_scales_pages = jnp.broadcast_to(
        v_scales_pages, (*v_scales_pages.shape[:-1], v_pages.shape[-1])
    )
  else:
    v_scales_pages = None

  batch_size, num_q_heads, head_dim = q.shape
  num_kv_heads, _, page_size, head_dim_k = k_pages.shape
  batch_size_paged_indices, pages_per_sequence = page_indices.shape

  if k_pages.shape != v_pages.shape:
    raise ValueError(
        f"k_pages and v_pages must have the same shape. Got {k_pages.shape} and"
        f" {v_pages.shape}"
    )
  if num_q_heads % num_kv_heads != 0:
    raise ValueError(
        "Number of Q heads must be divisible by number of KV heads. Got"
        f" {num_q_heads} and {num_kv_heads}."
    )
  if head_dim_k != head_dim:
    raise ValueError(
        "head_dim of Q must be the same as that of K/V. Got"
        f" {head_dim} and {head_dim_k}."
    )
  if pages_per_sequence % pages_per_compute_block != 0:
    raise ValueError(
        "pages_per_compute_block must be divisible by pages per sequence. Got"
        f" {pages_per_compute_block} and {pages_per_sequence}."
    )
  if lengths.shape != (batch_size,):
    raise ValueError("`lengths` and `q` must have the same batch size")
  if batch_size_paged_indices != batch_size:
    raise ValueError("`page_indices` and `q` must have the same batch size")
  if lengths.dtype != jnp.int32:
    raise ValueError(
        f"The dtype of `lengths` must be int32. Got {lengths.dtype}"
    )

  # TODO(dinghua): get the actual cores per chip once there's an official API.
  if megacore_mode == "kv_head":
    if num_kv_heads % 2 != 0:
      raise ValueError(
          "number of KV heads must be even when megacore_mode is 'kv_head'"
      )
    num_cores = 2
  elif megacore_mode == "batch":
    if batch_size % 2 != 0:
      raise ValueError("batch size must be even when megacore_mode is 'batch'")
    num_cores = 2
  elif megacore_mode is None:
    num_cores = 1
  else:
    raise ValueError("megacore_mode must be one of ['kv_head', 'batch', None]")

  num_groups = num_q_heads // num_kv_heads
  if (num_groups) % 8 != 0:
    # Reshape q to hint XLA to pick a <1x128> layout otherwise it will pick a
    # <8x128> layout for a <1x128> memref inside the kernel and error out.
    q = q.reshape(batch_size, num_q_heads, 1, head_dim)
    if megacore_mode == "kv_head":
      q_block_spec = pl.BlockSpec(
          (None, num_groups, None, head_dim),
          lambda core_index, b, h, *_: (b, h * num_cores + core_index, 0, 0),
      )
    elif megacore_mode == "batch":
      q_block_spec = pl.BlockSpec(
          (None, num_groups, None, head_dim),
          lambda core_index, b, h, *_: (b * num_cores + core_index, h, 0, 0),
      )
    else:
      q_block_spec = pl.BlockSpec(
          (None, num_groups, None, head_dim),
          lambda core_index, b, h, *_: (b, h, 0, 0),
      )
    q_dtype_for_kernel_launch = jnp.float32
  else:
    if megacore_mode == "kv_head":
      q_block_spec = pl.BlockSpec(
          (None, num_groups, head_dim),
          lambda core_index, b, h, *_: (b, h * num_cores + core_index, 0),
      )
    elif megacore_mode == "batch":
      q_block_spec = pl.BlockSpec(
          (None, num_groups, head_dim),
          lambda core_index, b, h, *_: (b * num_cores + core_index, h, 0),
      )
    else:
      q_block_spec = pl.BlockSpec(
          (None, num_groups, head_dim),
          lambda core_index, b, h, *_: (b, h, 0),
      )
    q_dtype_for_kernel_launch = q.dtype

  dimension_semantics: Sequence[Literal["parallel", "arbitrary"]]
  if inline_seq_dim:
    kernel = paged_flash_attention_kernel_inline_seq_dim
    grid = (
        num_cores,
        batch_size // num_cores if megacore_mode == "batch" else batch_size,
        num_kv_heads // num_cores
        if megacore_mode == "kv_head"
        else num_kv_heads,
    )
    dimension_semantics = ("parallel", "arbitrary", "arbitrary")
  else:
    kernel = paged_flash_attention_kernel
    grid = (
        num_cores,
        batch_size // num_cores if megacore_mode == "batch" else batch_size,
        num_kv_heads // num_cores
        if megacore_mode == "kv_head"
        else num_kv_heads,
        pages_per_sequence // pages_per_compute_block,
    )
    dimension_semantics = ("parallel", "arbitrary", "arbitrary", "arbitrary")

  if k_scales_pages is not None and v_scales_pages is not None:
    in_specs = [
        q_block_spec,
        pl.BlockSpec(memory_space=pl.ANY),
        pl.BlockSpec(memory_space=pl.ANY),
        pl.BlockSpec(memory_space=pl.ANY),
        pl.BlockSpec(memory_space=pl.ANY),
    ]
    scratch_shapes = (
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            k_pages.dtype,
        ),  # k_pages buffer
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            k_scales_pages.dtype,
        ),  # k_scales_pages buffer
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            v_pages.dtype,
        ),  # v_pages buffer
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            v_scales_pages.dtype,
        ),  # v_scales_pages buffer
        pltpu.SemaphoreType.DMA((2,)),
        pltpu.SemaphoreType.DMA((2,)),
    )
  else:
    in_specs = [
        q_block_spec,
        pl.BlockSpec(memory_space=pl.ANY),
        None,
        pl.BlockSpec(memory_space=pl.ANY),
        None,
    ]
    scratch_shapes = (
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            k_pages.dtype,
        ),  # k_pages buffer
        None,
        pltpu.VMEM(
            (
                2,  # For double buffering during DMA copies.
                pages_per_compute_block,
                page_size,
                head_dim,
            ),
            v_pages.dtype,
        ),  # v_pages buffer
        None,
        pltpu.SemaphoreType.DMA((2,)),
        pltpu.SemaphoreType.DMA((2,)),
    )

  out, _, _ = pl.pallas_call(
      functools.partial(
          kernel,
          pages_per_sequence=pages_per_sequence,
          batch_size=batch_size,
          pages_per_compute_block=pages_per_compute_block,
          mask_value=mask_value,
          attn_logits_soft_cap=attn_logits_soft_cap,
          megacore_mode=megacore_mode,
      ),
      grid_spec=pltpu.PrefetchScalarGridSpec(
          # There are 4 scalars prefetched per kernel call: `lengths_ref`,
          # `page_indices_ref`, `buffer_index_ref`, `init_flag_ref`
          num_scalar_prefetch=4,
          in_specs=in_specs,
          out_specs=[
              q_block_spec,
              q_block_spec,
              q_block_spec,
          ],
          grid=grid,
          scratch_shapes=scratch_shapes,
      ),
      compiler_params=pltpu.CompilerParams(
          dimension_semantics=dimension_semantics
      ),
      out_shape=[
          jax.ShapeDtypeStruct(q.shape, q_dtype_for_kernel_launch),
          jax.ShapeDtypeStruct((*q.shape[:-1], 1), jnp.float32),
          jax.ShapeDtypeStruct((*q.shape[:-1], 1), jnp.float32),
      ],
  )(
      lengths,
      page_indices.reshape(-1),
      jnp.zeros((1,), jnp.int32),  # buffer index
      jnp.ones((1,), jnp.int32),  # init flag
      q.astype(q_dtype_for_kernel_launch),
      k_pages,
      k_scales_pages,
      v_pages,
      v_scales_pages,
  )
  return out.reshape(batch_size, num_q_heads, head_dim).astype(q.dtype)

