import functools
import random
from typing import Callable
import math


def dot_product_attention(
    query: Array,
    key: Array,
    value: Array,
    bias: Array | None = None,
    mask: Array | None = None,
    q_seqlen: Array | None = None,
    kv_seqlen: Array | None = None,
    q_offsets: Array | None = None,
    kv_offsets: Array | None = None,
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
  """Computes dot-product attention given query (Q), key (K), and value (V).

  This function serves as the core operation for applying attention
  mechanisms as described in the paper [https://arxiv.org/abs/1706.03762].
  Initially, it determines the attention weights by processing Q and K,
  subsequently combining the outcomes using K. Throughout this function, we
  utilize the following uppercase letters to represent specific parameters of
  array:

    B = batch size
    S = length of the key/value (source)
    T = length of the query (target)
    N = number of attention heads
    H = dimensions of each attention head.

  The supported layouts for Q, K, V are either BT(S)NH or BNT(S)H, and they must
  adhere to the same layout. The output layout remains consistent with Q,
  defaulting to BT(S)NH.

  Args:
    query: Queries for attention calculation with a shape of BTNH or BNTH.
    key: Keys for attention calculation with a shape of BSNH or BNSH.
    value: Values to be used in attention with a shape of BSNH or BNSH.
    bias: Bias to be added to logits with a shape of BNTS.
    mask: Mask used to filter out logits with a shape of BNTS.
    q_seqlen: Non padded sequence length of query with a shape of B.
      If q_offsets is set, q_seqlen should have shape [B,M] where M is the
      maximum number of segments per batch. For batch that has less segments
      than maximum segments, fill the padded entries with -1.
    kv_seqlen: Non padded sequence length of key and value with a shape of B.
      If kv_offsets is set, kv_seqlen should have shape [B,M] where M is the
      maximum number of segments per batch. For batch that has less segments
      than maximum segments, fill the padded entries with -1.
    q_offsets: offset of each segment packed in query with a shape of [B,M+1]
      where M is the maximum number of segments per batch. For batch that has
      less segments than maximum segments, fill the padded entries with -1.
      E.g, if 2 batches has 3 and 2 segments respectively, each segment has
      size 1, q_offsets = [[0,1,2,-1], [0,1,-1,-1]]. q_seqlen should be set
      to indicate the size of each segment.
    kv_offsets: offset of each segment packed in key with a shape of [B,M+1]
      where M is the maximum number of segments per batch. For batch that has
      less segments than maximum segments, fill the padded entries with -1.
      E.g, if 2 batches has 3 and 2 segments respectively, each segment has
      size 1, kv_offsets = [[0,1,2,-1], [0,1,-1,-1]]. kv_seqlen should be set
      to indicate the size of each segment.
    scale: Scale for the query.
    dropout_rate: Dropout rate.
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
    amax_s: amax of state. (fp8 only)
    amax_o: amax of output. (fp8 only)
  """
  # TODO(b/380898464): Check the compute capability, e.g., require GPU device,
  # in the kernel implementation (c++) code.
  cudnn_version = check_cudnn_version()
  layout = _normalize_layout(qkv_layout)

  if use_fp8:
    if fp8_params is None:
      raise ValueError("fp8_params should not be None.")
    if  mask_type not in (MaskType.NO_MASK, MaskType.CAUSAL):
      raise ValueError("Only NO_MASK or CAUSAL masks are supported for fp8.")
    if not all(x is None for x in [bias, mask, q_seqlen, kv_seqlen]):
      raise ValueError(
          f"Expected 'None' for bias, mask, q_seqlen, and kv_seqlen, "
          f"but got: bias={bias}, mask={mask}, q_seqlen={q_seqlen}, kv_seqlen={kv_seqlen}"
      )
    check_fp8_params(fp8_params)
    check_layout(query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      None, None, layout)
    output, amax_s, amax_o = _dot_product_attention_fp8(
        query, key, value, fp8_params,
        scale, mask_type == MaskType.CAUSAL, layout.value, cudnn_version
    )
    return output, amax_s, amax_o
  else:
    if has_padding(mask_type) and (q_seqlen is None or kv_seqlen is None):
        raise ValueError("Require q_seqlen and kv_seqlen to generate padding mask")
    if sliding_window_length is not None and sliding_window_length <= 0:
      raise ValueError(
        f"Require sliding_window_length > 0, got {sliding_window_length}")
    if q_offsets is not None and (q_seqlen is None or kv_seqlen is None):
      raise ValueError("Require q_seqlen and kv_seqlen to use packed layout")

    bias = combine_bias_and_mask(bias, mask, query.dtype)
    # check if input shape and data type is compatiable
    check_layout(query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      None, None, layout)
    has_bias = bias is not None
    has_dbias = has_bias and \
      should_export_dbias(bias.shape, query.shape, layout)
    variadic_args = (has_bias, has_dbias)

    _not_used = jnp.zeros(0, dtype=query.dtype)
    if bias is None:
      bias = _not_used
    if q_seqlen is None:
      q_seqlen = _not_used
    if kv_seqlen is None:
      kv_seqlen = _not_used
    if q_offsets is None:
      q_offsets = _not_used
    if kv_offsets is None:
      kv_offsets = _not_used

    output = _dot_product_attention(
        query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
        _not_used, _not_used, scale, seed, dropout_rate, variadic_args,
        mask_type, layout.value, sliding_window_length, cudnn_version,
        return_residual)
    return output


def dot_product_attention(
    query: ArrayLike,
    key: ArrayLike,
    value: ArrayLike,
    bias: ArrayLike | None = None,
    mask: ArrayLike | None = None,
    *,
    scale: float | None = None,
    is_causal: bool = False,
    query_seq_lengths: ArrayLike | None = None,
    key_value_seq_lengths: ArrayLike | None = None,
    local_window_size: int | tuple[int, int] | None = None,
    implementation: Literal['xla', 'cudnn'] | None = None,
    return_residual: Literal[False] = ...,
) -> Array: ...


def dot_product_attention(
    query: ArrayLike,
    key: ArrayLike,
    value: ArrayLike,
    bias: ArrayLike | None = None,
    mask: ArrayLike | None = None,
    *,
    scale: float | None = None,
    is_causal: bool = False,
    query_seq_lengths: ArrayLike | None = None,
    key_value_seq_lengths: ArrayLike | None = None,
    local_window_size: int | tuple[int, int] | None = None,
    implementation: Literal['xla', 'cudnn'] | None = None,
    return_residual: Literal[True] = ...,
) -> tuple[Array, Array]: ...


def dot_product_attention(
    query: ArrayLike,
    key: ArrayLike,
    value: ArrayLike,
    bias: ArrayLike | None = None,
    mask: ArrayLike | None = None,
    *,
    scale: float | None = None,
    is_causal: bool = False,
    query_seq_lengths: ArrayLike | None = None,
    key_value_seq_lengths: ArrayLike | None = None,
    local_window_size: int | tuple[int, int] | None = None,
    implementation: Literal['xla', 'cudnn'] | None = None,
    return_residual: bool = False,
):
  r"""Scaled dot product attention function.

  Computes the following for each head:

  .. math::

    \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left( \frac{QK^T}{\sqrt{d}} + B \right) V

  where
  :math:`Q` is the query matrix,
  :math:`K` is the key matrix,
  :math:`V` is the value matrix,
  :math:`d` is the dimension of each individual query and key,
  and :math:`B` is the bias matrix (optional).

  Throughout this function, we utilize the following uppercase letters to
  represent the shape of array::

    B = batch size
    S = length of the key/value (source)
    T = length of the query (target)
    N = number of attention heads
    H = dimensions of each attention head
    K = number of key/value heads
    G = number of groups, which equals to N // K

  Args:
    query: query array; shape :code:`(BTNH|TNH)`
    key: key array: shape :code:`(BSKH|SKH)`. When `K` equals `N`, multi-headed
      attention (MHA https://arxiv.org/abs/1706.03762) is performed. Otherwise,
      grouped query attention (GQA https://arxiv.org/abs/2305.13245) is
      performed if `N` is a multiple of `K`, and multi-query attention (MQA
      https://arxiv.org/abs/1911.02150) is performed if `K == 1` (a special case
      of GQA).
    value: value array, should have the same shape as the `key` array.
    bias: optional, bias array to be added to logits; The shape must be 4D and
      be broadcastable to :code:`(BNTS|NTS)`.
    mask: optional, mask array used to filter out logits. It is a boolean mask
      where `True` indicates the element should take part in attention. For an
      additive mask, users should pass it to `bias`. The shape must be 4D and be
      broadcastable to :code:`(BNTS|NTS)`.
    scale: scale for the logits. If None, the scale will be set to 1 divided by
      the square root of query's head dimension (i.e. H).
    is_causal: If true, causal attention will be applied. Note, some
      implementations like `xla` will generate a mask tensor and apply it to the
      logits to mask out the non-causal parts of the attention matrix, but other
      implementations like `cudnn` will avoid computing the non-causal regions,
      providing speedups.
    query_seq_lengths: `int32` array of sequence lengths for query; shape
      :code:`(B)`
    key_value_seq_lengths: `int32` array of sequence lengths for key and value;
      shape :code:`(B)`
    local_window_size: Window sizes to make self attention to attend to each
      token's local window. If set, this specifies the (left_window_size,
      right_window_size) for each token. E.g., if local_window_size == (3, 2)
      and the sequence is [0, 1, 2, 3, 4, 5, c, 7, 8, 9], token `c` can attend
      to [3, 4, 5, c, 7, 8]. If a single int is given, it will be interpreted as
      a symmetric window (window_size, window_size).
    return_residual: Whether to return the logsumexp tensor of shape BTN
      or BNT to users. See section 3.1.1 in the FlashAttention-2 paper:
      https://arxiv.org/pdf/2307.08691 to find the definition of logsumexp.
    implementation: A string to control which implementation backend to use.
      Supported strings are `xla`, `cudnn` (cuDNN flash attention). It defaults
      to `None`, which currently falls back to `xla`.
      Note, `cudnn` supports only a subset of shapes/dtypes, and an exception
      will be thrown if its not supported.

  Returns:
    If return_residual is False, returns an array of the attention output with
    the same shape as :code:`query`. If return_residual is True, returns a tuple
    of (output, residual). The residual is the shape of BTN|TN.
  """
  output_shape = jnp.asarray(query).shape
  residual_shape = output_shape[:-1]
  def _ensure_4d(t):
    t = jnp.asarray(t)
    dims_to_add = 4 - t.ndim
    if dims_to_add > 0:
      return jnp.expand_dims(t, axis=tuple(range(dims_to_add)))
    return t

  query_arr = _ensure_4d(query)
  key_arr = _ensure_4d(key)
  value_arr = _ensure_4d(value)
  bias = _ensure_4d(bias) if bias is not None else None
  mask = _ensure_4d(mask) if mask is not None else None
  if query_seq_lengths is not None:
    query_seq_lengths = jnp.asarray(query_seq_lengths)
  if key_value_seq_lengths is not None:
    key_value_seq_lengths = jnp.asarray(key_value_seq_lengths)
  if isinstance(local_window_size, int):
    local_window_size = (local_window_size, local_window_size)

  def _check_shape_and_dtype(t: Array | None, shape: Sequence[int],
                             dtype: DType | None, name: str) -> None:
    if t is None:
      return
    if t.ndim != len(shape):
      raise ValueError(f"{name} ndim should be {len(shape)}, but got {t.ndim}")
    if dtype is not None and t.dtype != dtype:
      raise ValueError(f"{name} dtype should be {dtype}, but got {t.dtype}")
    for i in range(t.ndim):
      if shape[i] != -1 and t.shape[i] != shape[i]:
        raise ValueError(f"{name} shape should be {shape}: but got {t.shape}")

  B, S, K, H = key_arr.shape
  _check_shape_and_dtype(value_arr, [B, S, K, H], key_arr.dtype, 'value')
  _check_shape_and_dtype(query_arr, [B, -1, -1, H], key_arr.dtype, 'query')
  _check_shape_and_dtype(mask, [-1] * 4, np.dtype(bool), 'mask')
  _check_shape_and_dtype(bias, [-1] * 4, None, 'bias')
  _check_shape_and_dtype(query_seq_lengths, [B], np.dtype('int32'),
                         'query_seq_lengths')
  _check_shape_and_dtype(key_value_seq_lengths, [B], np.dtype('int32'),
                         'key_value_seq_lengths')
  if query_arr.shape[-2] % K != 0:
    raise ValueError(f"The number of query heads must be a multiple of "
                     f"key/value heads, but got {query_arr.shape[-2]} vs {K}")

  scale_val = (1.0 / np.sqrt(H)) if scale is None else scale

  match implementation:
    case 'xla':
      out = _dot_product_attention_xla(
          query_arr, key_arr, value_arr, bias, mask, is_causal=is_causal,
          scale=scale_val, q_seqlen=query_seq_lengths,
          kv_seqlen=key_value_seq_lengths,
          local_window_size=local_window_size,
          return_residual=return_residual,
      )
    case 'cudnn':
      use_padding = (
           query_seq_lengths is not None or key_value_seq_lengths is not None
      )
      if use_padding:
        if query_seq_lengths is None:
          T = query_arr.shape[1]
          query_seq_lengths = jnp.full((B,), T, dtype=np.int32)
        if key_value_seq_lengths is None:
          key_value_seq_lengths = jnp.full((B,), S, dtype=np.int32)

      mask_type = MaskType.NO_MASK
      if use_padding and is_causal:
        mask_type = MaskType.PADDING_CAUSAL
      elif is_causal:
        mask_type = MaskType.CAUSAL
      elif use_padding:
        mask_type = MaskType.PADDING
      # CuDNN supports only the left window with an exclusive boundary when
      # causal mask is enabled.
      sliding_window = None
      if local_window_size is not None:
        l_window, r_window = local_window_size
        if r_window == 0 or mask_type == MaskType.CAUSAL:
          sliding_window = l_window + 1
        else:
          raise ValueError(f"cuDNN doesn't support right window: {r_window} "
                           "when causal mask is not used.")

      out = cudnn_dot_product_attention(
          query_arr, key_arr, value_arr, bias, mask, query_seq_lengths,
          key_value_seq_lengths, scale=scale_val, mask_type=mask_type,
          sliding_window_length=sliding_window, return_residual=return_residual,
      )
      if return_residual:
        # Regardless of input layout, cudnn always returns residual with
        # (B N T) layout.
        out, residual = out
        residual = jnp.transpose(residual, (0, 2, 1)).astype(out.dtype)
        out = (out, residual)
    case None:
      # TODO(kaixih@nvidia) Automatically select the best backend (defaults to XLA for now).
      out = _dot_product_attention_xla(
          query_arr, key_arr, value_arr, bias, mask, is_causal=is_causal,
          scale=scale_val, q_seqlen=query_seq_lengths,
          kv_seqlen=key_value_seq_lengths,
          local_window_size=local_window_size,
          return_residual=return_residual,
      )
    case _:
      raise ValueError(f"Unsupported implementation option: {implementation}")

  if return_residual:
    out, residual = out
    return jnp.reshape(out, output_shape), jnp.reshape(residual, residual_shape)

  return jnp.reshape(out, output_shape)


def dot_product_attention(
    query: Array,
    key: Array,
    value: Array,
    bias: Array | None = None,
    mask: Array | None = None,
    broadcast_dropout: bool = True,
    dropout_rng: PRNGKey | None = None,
    dropout_rate: float = 0.0,
    deterministic: bool = False,
    dtype: Dtype | None = None,
    precision: PrecisionLike = None,
    module: Module | None = None,
    force_fp32_for_softmax: bool = False,
    einsum_dot_general: Callable[..., Array] | None = None,
    qk_attn_weights_einsum: Callable[..., Array] | None = None,
    attn_weights_value_einsum: Callable[..., Array] | None = None,
):
  """Computes dot-product attention given query, key, and value.

  This is the core function for applying attention based on
  https://arxiv.org/abs/1706.03762. It calculates the attention weights given
  query and key and combines the values using the attention weights.

  .. note::
    ``query``, ``key``, ``value`` needn't have any batch dimensions.

  Args:
    query: queries for calculating attention with shape of ``[batch...,
      q_length, num_heads, qk_depth_per_head]``.
    key: keys for calculating attention with shape of ``[batch..., kv_length,
      num_heads, qk_depth_per_head]``.
    value: values to be used in attention with shape of ``[batch..., kv_length,
      num_heads, v_depth_per_head]``.
    bias: bias for the attention weights. This should be broadcastable to the
      shape ``[batch..., num_heads, q_length, kv_length]``. This can be used for
      incorporating causal masks, padding masks, proximity bias, etc.
    mask: mask for the attention weights. This should be broadcastable to the
      shape ``[batch..., num_heads, q_length, kv_length]``. This can be used for
      incorporating causal masks. Attention weights are masked out if their
      corresponding mask value is ``False``.
    broadcast_dropout: bool: use a broadcasted dropout along batch dims.
    dropout_rng: JAX PRNGKey: to be used for dropout
    dropout_rate: dropout rate
    deterministic: bool, deterministic or not (to apply dropout)
    dtype: the dtype of the computation (default: infer from inputs)
    precision: numerical precision of the computation see ``jax.lax.Precision`
      for details.
    module: the Module that will sow the attention weights into the
      'intermediates' collection. Remember to mark 'intermediates' as mutable
      via ``mutable=['intermediates']`` in order to have that collection
      returned. If ``module`` is None, the attention weights will not be sowed.
    force_fp32_for_softmax: bool, whether to force the softmax to be computed in
      fp32. This is useful for mixed-precision training where higher precision
      is desired for numerical stability.
    einsum_dot_general: the dot_general to use in `jnp.einsum`.
    qk_attn_weights_einsum: the einsum for computing the attention weights. When
      unspecified, the default `jnp.einsum` will be used. This argument is
      mutually exclusive with `precision` and `einsum_dot_general`.
    attn_weights_value_einsum: the einsum for computing the product of the
      attention weights and the values. When unspecified, the default
      `jnp.einsum` will be used. This argument is mutually exclusive with
      `precision` and `einsum_dot_general`.

  Returns:
    Output of shape ``[batch..., q_length, num_heads, v_depth_per_head]``.

  Raises:
    ValueError: if both `precision`/`einsum_dot_general` and
    `qk_attn_weights_einsum`/`attn_weights_value_einsum` are
      specified.
  """
  if (qk_attn_weights_einsum and not attn_weights_value_einsum) or (
      not qk_attn_weights_einsum and attn_weights_value_einsum
  ):
    raise ValueError(
        'qk_attn_weights_einsum and attn_weights_value_einsum must be specified'
        ' together.'
    )
  if (precision or einsum_dot_general) and (
      qk_attn_weights_einsum or attn_weights_value_einsum
  ):
    raise ValueError(
        'precision/einsum_dot_general and'
        ' qk_attn_weights_einsum/attn_weights_value_einsum are mutually'
        ' exclusive. Please specify only one of them.'
    )

  query, key, value = promote_dtype(query, key, value, dtype=dtype)
  dtype = query.dtype
  assert key.ndim == query.ndim == value.ndim, 'q, k, v must have same rank.'
  assert (
    query.shape[:-3] == key.shape[:-3] == value.shape[:-3]
  ), 'q, k, v batch dims must match.'
  assert (
    query.shape[-2] == key.shape[-2] == value.shape[-2]
  ), 'q, k, v num_heads must match.'
  assert key.shape[-3] == value.shape[-3], 'k, v lengths must match.'

  # compute attention weights
  attn_weights = dot_product_attention_weights(
      query,
      key,
      bias,
      mask,
      broadcast_dropout,
      dropout_rng,
      dropout_rate,
      deterministic,
      dtype,
      precision,
      module,
      force_fp32_for_softmax,
      einsum_dot_general=einsum_dot_general,
      einsum=qk_attn_weights_einsum,
  )
  if not attn_weights_value_einsum:
    attn_weights_value_einsum = functools.partial(
        jnp.einsum,
        precision=precision,
        _dot_general=einsum_dot_general
        if einsum_dot_general
        else jax.lax.dot_general,
    )
  # return weighted sum over values for each query position
  return attn_weights_value_einsum(
      '...hqk,...khd->...qhd',
      attn_weights,
      value,
  )


def dot_product_attention(
  query: Array,
  key: Array,
  value: Array,
  bias: Array | None = None,
  mask: Array | None = None,
  broadcast_dropout: bool = True,
  dropout_rng: Array | None = None,
  dropout_rate: float = 0.0,
  deterministic: bool = False,
  dtype: Dtype | None = None,
  precision: PrecisionLike = None,
  module: Module | None = None,
  promote_dtype: PromoteDtypeFn = dtypes.promote_dtype,
  is_causal: bool = False,
):
  """Computes dot-product attention given query, key, and value.

  This is the core function for applying attention based on
  https://arxiv.org/abs/1706.03762. It calculates the attention weights given
  query and key and combines the values using the attention weights.

  Will use the more optimized `jax.nn.dot_product_attention` if dropout is
  not activated and `module=None`.

  .. note::
    ``query``, ``key``, ``value`` needn't have any batch dimensions.

  Args:
    query: queries for calculating attention with shape of ``[batch..., q_length,
      num_heads, qk_depth_per_head]``.
    key: keys for calculating attention with shape of ``[batch..., kv_length,
      num_heads, qk_depth_per_head]``.
    value: values to be used in attention with shape of ``[batch..., kv_length,
      num_heads, v_depth_per_head]``.
    bias: bias for the attention weights. This should be broadcastable to the
      shape `[batch..., num_heads, q_length, kv_length]`. This can be used for
      incorporating causal masks, padding masks, proximity bias, etc.
    mask: mask for the attention weights. This should be broadcastable to the
      shape `[batch..., num_heads, q_length, kv_length]`. This can be used for
      incorporating causal masks. Attention weights are masked out if their
      corresponding mask value is `False`.
    broadcast_dropout: bool: use a broadcasted dropout along batch dims.
    dropout_rng: JAX PRNGKey: to be used for dropout
    dropout_rate: dropout rate
    deterministic: bool, deterministic or not (to apply dropout)
    dtype: the dtype of the computation (default: infer from inputs)
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.
    module: the Module that will sow the attention weights into the
      ``nnx.Intermediate`` collection. If ``module`` is None, the attention
      weights will not be sowed.
    promote_dtype: function to promote the dtype of the arrays to the desired
      dtype. The function should accept a tuple of ``(query, key, value)`` and a
      ``dtype`` keyword argument, and return a tuple of arrays with the promoted
      dtype.
    is_causal: If true, causal attention will be applied. Note, some
      implementations like xla will generate a mask tensor and apply it to
      the logits to mask out the non-causal parts of the attention matrix,
      but other implementations like cudnn will avoid computing the
      non-causal regions, providing speedups.

  Returns:
    Output of shape `[batch..., q_length, num_heads, v_depth_per_head]`.
  """
  query, key, value = promote_dtype((query, key, value), dtype=dtype)  # type: ignore[bad-unpacking]
  dtype = query.dtype

  assert key.ndim == query.ndim == value.ndim, 'q, k, v must have same rank.'
  assert (
    query.shape[:-3] == key.shape[:-3] == value.shape[:-3]
  ), 'q, k, v batch dims must match.'
  assert key.shape[-3] == value.shape[-3], 'k, v lengths must match.'

  # Criteria that invoke the more optimized dot product attention
  if dropout_rate == 0.0 and module is None:
    # make sure qkv batch are compressed to one dim
    query_shape = query.shape
    if len(query_shape) > 4:
      def reshape_4d(x):
        return jnp.reshape(x, (math.prod(x.shape[:-3]), *x.shape[-3:]))
      query, key, value, bias, mask = jax.tree.map(
        reshape_4d, (query, key, value, bias, mask))
    if mask is not None:
      mask = mask.astype(jnp.bool)
    out = jax.nn.dot_product_attention(query, key, value, bias, mask, is_causal=is_causal)
    if len(query_shape) > 4:
      out = jnp.reshape(out, query_shape)
    return out

  # compute attention weights
  attn_weights = dot_product_attention_weights(
    query,
    key,
    bias,
    mask,
    broadcast_dropout,
    dropout_rng,
    dropout_rate,
    deterministic,
    dtype,
    precision,
    module,
    promote_dtype,
    is_causal,
  )

  # return weighted sum over values for each query position
  # check if need to broadcast Value heads to match Query heads (GQA)
  if attn_weights.shape[-3] != value.shape[-2]:
      q_heads = attn_weights.shape[-3]
      v_heads = value.shape[-2]
      if q_heads % v_heads != 0:
         raise ValueError(f"Query heads ({q_heads}) must be multiple of Value heads ({v_heads})")

      n_rep = q_heads // v_heads
      # Reshape weights: [..., H_v, n_rep, Q, K]
      attn_weights = attn_weights.reshape(attn_weights.shape[:-3] + (v_heads, n_rep) + attn_weights.shape[-2:])
      # Expand Value: [..., K, H_v, 1, D]
      value = jnp.expand_dims(value, axis=-2)
      # Contract: hgqk, kh1d -> qhgd (h=H_v, g=n_rep)
      out = jnp.einsum('...hgqk,...kh1d->...qhgd', attn_weights, value, precision=precision)
      # Flatten: [..., Q, H_q, D]
      out = out.reshape(out.shape[:-3] + (q_heads, out.shape[-1]))
  else:
      out = jnp.einsum(
        '...hqk,...khd->...qhd', attn_weights, value, precision=precision
      )

  return out


def dot_product_attention(
  scope,
  query,
  key,
  value,
  dtype=jnp.float32,
  bias=None,
  axis=None,
  broadcast_dropout=True,
  dropout_rng=None,
  dropout_rate=0.0,
  deterministic=False,
  precision=None,
):
  """Computes dot-product attention given query, key, and value.

  This is the core function for applying attention based on
  https://arxiv.org/abs/1706.03762. It calculates the attention weights given
  query and key and combines the values using the attention weights. This
  function supports multi-dimensional inputs.


  Args:
    query: queries for calculating attention with shape of `[batch_size, dim1,
      dim2, ..., dimN, num_heads, mem_channels]`.
    key: keys for calculating attention with shape of `[batch_size, dim1, dim2,
      ..., dimN, num_heads, mem_channels]`.
    value: values to be used in attention with shape of `[batch_size, dim1,
      dim2,..., dimN, num_heads, value_channels]`.
    dtype: the dtype of the computation (default: float32)
    bias: bias for the attention weights. This can be used for incorporating
      autoregressive mask, padding mask, proximity bias.
    axis: axises over which the attention is applied.
    broadcast_dropout: bool: use a broadcasted dropout along batch dims.
    dropout_rng: JAX PRNGKey: to be used for dropout
    dropout_rate: dropout rate
    deterministic: bool, deterministic or not (to apply dropout)
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.

  Returns:
    Output of shape `[bs, dim1, dim2, ..., dimN,, num_heads, value_channels]`.
  """
  assert key.shape[:-1] == value.shape[:-1]
  assert query.shape[0:1] == key.shape[0:1] and query.shape[-1] == key.shape[-1]

  if axis is None:
    axis = tuple(range(1, key.ndim - 2))
  if not isinstance(axis, Iterable):
    axis = (axis,)
  assert key.ndim == query.ndim
  assert key.ndim == value.ndim
  for ax in axis:
    if not (query.ndim >= 3 and 1 <= ax < query.ndim - 2):
      raise ValueError(
        'Attention axis must be between the batch axis and the last-two axes.'
      )
  depth = query.shape[-1]
  n = key.ndim
  # batch_dims is  <bs, <non-attention dims>, num_heads>
  batch_dims = tuple(np.delete(range(n), axis + (n - 1,)))
  # q & k -> (bs, <non-attention dims>, num_heads, <attention dims>, channels)
  qk_perm = batch_dims + axis + (n - 1,)
  key = key.transpose(qk_perm)
  query = query.transpose(qk_perm)
  # v -> (bs, <non-attention dims>, num_heads, channels, <attention dims>)
  v_perm = batch_dims + (n - 1,) + axis
  value = value.transpose(v_perm)

  query = query / jnp.sqrt(depth).astype(dtype)
  batch_dims_t = tuple(range(len(batch_dims)))
  attn_weights = lax.dot_general(
    query,
    key,
    (((n - 1,), (n - 1,)), (batch_dims_t, batch_dims_t)),
    precision=precision,
  )

  # apply attention bias: masking, droput, proximity bias, ect.
  if bias is not None:
    attn_weights = attn_weights + bias

  # normalize the attention weights
  norm_dims = tuple(range(attn_weights.ndim - len(axis), attn_weights.ndim))
  attn_weights = lax.exp(
    attn_weights
    - jax.scipy.special.logsumexp(attn_weights, axis=norm_dims, keepdims=True)
  )
  attn_weights = attn_weights.astype(dtype)

  # apply dropout
  if not deterministic and dropout_rate > 0.0:
    if dropout_rng is None:
      dropout_rng = scope.make_rng('dropout')
    keep_prob = 1.0 - dropout_rate
    if broadcast_dropout:
      # dropout is broadcast across the batch+head+non-attention dimension
      dropout_dims = attn_weights.shape[-(2 * len(axis)) :]
      dropout_shape = tuple([1] * len(batch_dims_t)) + dropout_dims
      keep = random.bernoulli(dropout_rng, keep_prob, dropout_shape)
    else:
      keep = random.bernoulli(dropout_rng, keep_prob, attn_weights.shape)
    multiplier = keep.astype(attn_weights.dtype) / jnp.asarray(
      keep_prob, dtype=dtype
    )
    attn_weights = attn_weights * multiplier

  # compute the new values given the attention weights
  wv_contracting_dims = (norm_dims, range(value.ndim - len(axis), value.ndim))
  y = lax.dot_general(
    attn_weights,
    value,
    (wv_contracting_dims, (batch_dims_t, batch_dims_t)),
    precision=precision,
  )

  # back to (bs, dim1, dim2, ..., dimN, num_heads, channels)
  perm_inv = _invert_perm(qk_perm)
  y = y.transpose(perm_inv)
  return y

