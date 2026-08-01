
def dot_product_attention_weights(
    query: Array,
    key: Array,
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
    einsum: Callable[..., Array] | None = None,
):
  """Computes dot-product attention weights given query and key.

  Used by :func:`dot_product_attention`, which is what you'll most likely use.
  But if you want access to the attention weights for introspection, then
  you can directly call this function and call einsum yourself.

  Args:
    query: queries for calculating attention with shape of ``[batch...,
      q_length, num_heads, qk_depth_per_head]``.
    key: keys for calculating attention with shape of ``[batch..., kv_length,
      num_heads, qk_depth_per_head]``.
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
    dtype: the dtype of the computation (default: infer from inputs and params)
    precision: numerical precision of the computation see ``jax.lax.Precision``
      for details.
    module: the Module that will sow the attention weights into the
      'intermediates' collection. Remember to mark 'intermediates' as mutable
      via ``mutable=['intermediates']`` in order to have that collection
      returned. If ``module`` is None, the attention weights will not be sowed.
    force_fp32_for_softmax: bool, whether to force the softmax to be computed in
      fp32. This is useful for mixed-precision training where higher precision
      is desired for numerical stability.
    einsum_dot_general: the dot_general to use in einsum.
    einsum: If unspecified, default `jnp.einsum` will be used. This argument is
      mutually exclusive with `precision` and `einsum_dot_general`.

  Raises:
    ValueError: if both `precision`/`einsum_dot_general` and `einsum` are
      specified.

  Returns:
    Output of shape ``[batch..., num_heads, q_length, kv_length]``.
  """
  if (precision or einsum_dot_general) and einsum:
    raise ValueError(
        'precision/einsum_dot_general and einsum are mutually exclusive. Please'
        ' specify only one of them.'
    )
  if not einsum:
    einsum = functools.partial(
        jnp.einsum,
        precision=precision,
        _dot_general=einsum_dot_general
        if einsum_dot_general
        else jax.lax.dot_general,
    )

  query, key = promote_dtype(query, key, dtype=dtype)
  dtype = query.dtype

  assert query.ndim == key.ndim, 'q, k must have same rank.'
  assert query.shape[:-3] == key.shape[:-3], 'q, k batch dims must match.'
  assert query.shape[-2] == key.shape[-2], 'q, k num_heads must match.'
  assert query.shape[-1] == key.shape[-1], 'q, k depths must match.'

  # calculate attention matrix
  depth = query.shape[-1]
  query = query / jnp.sqrt(depth).astype(dtype)
  # attn weight shape is (batch..., num_heads, q_length, kv_length)
  attn_weights = einsum('...qhd,...khd->...hqk', query, key)

  # apply attention bias: masking, dropout, proximity bias, etc.
  if bias is not None:
    attn_weights = attn_weights + bias
  # apply attention mask
  if mask is not None:
    big_neg = jnp.finfo(dtype).min
    attn_weights = jnp.where(mask, attn_weights, big_neg)

  # normalize the attention weights
  if force_fp32_for_softmax and dtype != jnp.float32:
    attn_weights = jax.nn.softmax(attn_weights.astype(jnp.float32))
  else:
    attn_weights = jax.nn.softmax(attn_weights).astype(dtype)

  if module:
    module.sow('intermediates', 'attention_weights', attn_weights)

  # apply attention dropout
  if not deterministic and dropout_rate > 0.0:
    keep_prob = 1.0 - dropout_rate
    if broadcast_dropout:
      # dropout is broadcast across the batch + head dimensions
      dropout_shape = tuple([1] * (key.ndim - 2)) + attn_weights.shape[-2:]
      keep = random.bernoulli(dropout_rng, keep_prob, dropout_shape)  # type: ignore
    else:
      keep = random.bernoulli(dropout_rng, keep_prob, attn_weights.shape)  # type: ignore
    multiplier = keep.astype(dtype) / jnp.asarray(keep_prob, dtype=dtype)
    attn_weights = attn_weights * multiplier

  return attn_weights


def dot_product_attention_weights(
  query: Array,
  key: Array,
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
  """Computes dot-product attention weights given query and key.

  Used by :func:`dot_product_attention`, which is what you'll most likely use.
  But if you want access to the attention weights for introspection, then
  you can directly call this function and call einsum yourself.

  Args:
    query: queries for calculating attention with shape of `[batch..., q_length,
      num_heads, qk_depth_per_head]`.
    key: keys for calculating attention with shape of `[batch..., kv_length,
      num_heads, qk_depth_per_head]`.
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
    dtype: the dtype of the computation (default: infer from inputs and params)
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.
    module: the Module that will sow the attention weights into the
      ``nnx.Intermediate`` collection. If ``module`` is None, the attention
      weights will not be sowed.
    promote_dtype: function to promote the dtype of the arrays to the desired
      dtype. The function should accept a tuple of ``(query, key)`` and a ``dtype``
      keyword argument, and return a tuple of arrays with the promoted dtype.
    is_causal: If true, causal attention will be applied. Note, some
      implementations like xla will generate a mask tensor and apply it to
      the logits to mask out the non-causal parts of the attention matrix,
      but other implementations like cudnn will avoid computing the
      non-causal regions, providing speedups.

  Returns:
    Output of shape `[batch..., num_heads, q_length, kv_length]`.
  """
  query, key = promote_dtype((query, key), dtype=dtype)  # type: ignore[bad-unpacking]
  dtype = query.dtype

  assert query.ndim == key.ndim, 'q, k must have same rank.'
  assert query.shape[:-3] == key.shape[:-3], 'q, k batch dims must match.'
  assert query.shape[-1] == key.shape[-1], 'q, k depths must match.'

  # check if we need to broadcast Key heads to match Query heads
  is_gqa = False
  if query.shape[-2] != key.shape[-2]:
    q_heads = query.shape[-2]
    k_heads = key.shape[-2]

    if q_heads % k_heads != 0:
      raise ValueError(
        f"Query heads ({q_heads}) must be multiple of "
        f"Key heads ({k_heads}) for Grouped Query Attention."
      )

    n_rep = q_heads // k_heads
    is_gqa = True
    # Reshape Query: [..., Q, H_k * n_rep, D] -> [..., Q, H_k, n_rep, D]
    query = query.reshape(query.shape[:-2] + (k_heads, n_rep, query.shape[-1]))
    # Expand Key: [..., K, H_k, D] -> [..., K, H_k, 1, D]
    key = jnp.expand_dims(key, axis=-2)

    # Contract: q(h)gd, k(h)1d -> hgqk (h=H_k, g=n_rep)
    einsum_str = '...qhgd,...kh1d->...hgqk'
  else:
    q_heads = query.shape[-2]
    einsum_str = '...qhd,...khd->...hqk'
    assert query.shape[-2] == key.shape[-2], 'q, k num_heads must match.'

  # calculate attention matrix
  depth = query.shape[-1]
  query = query / jnp.sqrt(depth).astype(dtype)

  # attn weight shape is (batch..., num_heads, q_length, kv_length)
  attn_weights = jnp.einsum(einsum_str, query, key, precision=precision)

  if is_gqa:
      attn_weights = attn_weights.reshape(attn_weights.shape[:-4] + (q_heads, attn_weights.shape[-2], attn_weights.shape[-1]))

  # apply attention bias: masking, dropout, proximity bias, etc.
  if bias is not None:
    attn_weights = attn_weights + bias
  # apply attention mask
  if mask is not None or is_causal:
    big_neg = jnp.finfo(dtype).min
    masks = [m for m in [mask] if m is not None]
    if is_causal:
      T, S = attn_weights.shape[-2:]
      causal_mask = jnp.tril(jnp.ones((T, S), dtype=dtype))
      target_shape = mask.shape if mask is not None else attn_weights.shape
      masks.append(jnp.broadcast_to(causal_mask, target_shape))
    combined_mask = combine_masks(*masks, dtype=dtype)
    assert combined_mask is not None
    attn_weights = jnp.where(combined_mask, attn_weights, big_neg)

  # normalize the attention weights
  attn_weights = jax.nn.softmax(attn_weights).astype(dtype)

  if module:
    module.sow(nnx.Intermediate, 'attention_weights', attn_weights)

  # apply attention dropout
  if not deterministic and dropout_rate > 0.0:
    keep_prob = 1.0 - dropout_rate
    # use original key.ndim because we might have expanded key dim
    ndim_base = key.ndim - 1 if is_gqa else key.ndim

    if broadcast_dropout:
      # dropout is broadcast across the batch + head dimensions
      dropout_shape = tuple([1] * (ndim_base - 2)) + attn_weights.shape[-2:]
      keep = random.bernoulli(dropout_rng, keep_prob, dropout_shape)  # type: ignore
    else:
      keep = random.bernoulli(dropout_rng, keep_prob, attn_weights.shape)  # type: ignore
    multiplier = keep.astype(dtype) / jnp.asarray(keep_prob, dtype=dtype)
    attn_weights = attn_weights * multiplier

  return attn_weights

