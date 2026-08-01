
def make_padding_mask(input_ids, padding_idx=1):
    """True for pad tokens"""
    padding_mask = input_ids.eq(padding_idx)
    if not padding_mask.any():
        padding_mask = None
    return padding_mask


def make_padding_mask(
  padding_mask_query,
  padding_mask_key,
  query_shape,
  key_shape,
  attention_axis=None,
  segmentation_mask=False,
):
  """Makes padding mask for attention weights.

  In case of 1d inputs (i.e., `[bs, len, features]`, the attention weights will
  be `[bs, len, len]` and this function makes a square matrix [len, len].

  Args:
    padding_mask_query: padding mask of query <bs, qdim1,.., qdimn>
    padding_mask_key: padding mask of query <bs, key1,.., keyn>
    query_shape: shape of the query
    key_shape: shape of the key, which is equal to the shape of value.
    attention_axis: axis over which attention is applied.
    segmentation_mask: bool: if true use equality on cartesian product rather
      than outer product for constructing segmentation masks.
  Returns:
    The padding mask for attention weights.
  """
  assert query_shape[0] == key_shape[0]
  assert len(query_shape) == len(key_shape)

  ndim = len(key_shape)
  if attention_axis is None:
    attention_axis = tuple(range(1, ndim - 2))
  assert isinstance(attention_axis, tuple)
  for ax in attention_axis:
    if not (ndim >= 3 and 1 <= ax < ndim - 2):
      raise ValueError(
        'Attention axis must be between the batch axis and the last-two axes.'
      )

  mask_shape_final = (query_shape[0], 1)  #  batch_size, 1 (for all heads)s
  for ax in attention_axis:
    mask_shape_final += (query_shape[ax],)
  for ax in attention_axis:
    mask_shape_final += (key_shape[ax],)

  padding_mask_query = padding_mask_query[..., None]
  padding_mask_key = padding_mask_key[..., None]
  perm = (0,) + tuple(np.flip(np.arange(padding_mask_key.ndim)))[:-1]
  if segmentation_mask:
    mask = jnp.equal(padding_mask_query, padding_mask_key.transpose(perm))
  else:
    mask = jnp.multiply(padding_mask_query, padding_mask_key.transpose(perm))

  mask = mask.reshape(mask_shape_final)
  mask = jax.lax.convert_element_type(mask, jnp.float32)
  return mask

