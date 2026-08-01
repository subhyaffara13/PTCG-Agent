
def _make_causal_mask(
    input_ids_shape: torch.Size, dtype: torch.dtype, device: torch.device, past_key_values_length: int = 0
):
    """
    Make causal mask used for bi-directional self-attention.
    """
    bsz, tgt_len = input_ids_shape
    mask = torch.full((tgt_len, tgt_len), torch.finfo(dtype).min, device=device)
    mask_cond = torch.arange(mask.size(-1), device=device)
    mask.masked_fill_(mask_cond < (mask_cond + 1).view(mask.size(-1), 1), 0)
    mask = mask.to(dtype)

    if past_key_values_length > 0:
        mask = torch.cat([torch.zeros(tgt_len, past_key_values_length, dtype=dtype, device=device), mask], dim=-1)
    return mask[None, None, :, :].expand(bsz, 1, tgt_len, tgt_len + past_key_values_length)


def _make_causal_mask(key, attention_axis=None, self_mask=False):
  """Makes a causal mask, to be used for masking out the future for attention.

  In case of 1d inputs (i.e., `[bs, len, features]`, the attention weights will
  be `[bs, len, len]` and this function makes a square matrix [len, len] with
  zeros in upper triangle and ones in lower triangle.

  Args:
    key: shape of the key, which is equal to the shape of value and is
      assumed to be equal to the shape of the query (since this is used in
      self-attention when decoding).
    attention_axis: axis over which attention is applied.
    self_mask: if mask out the diagonal or not.

  Returns:
    A causal mask to be used to mask out future positions.
  """
  if attention_axis is None:
    attention_axis = tuple(range(1, key.ndim - 2))
  assert isinstance(attention_axis, tuple)
  for ax in attention_axis:
    if not (key.ndim >= 3 and 1 <= ax < key.ndim - 2):
      raise ValueError(
        'Attention axis must be between the batch axis and the last-two axes.'
      )

  mask_shape = tuple([1] * (key.ndim - len(attention_axis) - 1))
  mask_shape_final = mask_shape
  for _ in range(2):
    flatten_dim = 1
    for ax in attention_axis:
      mask_shape_final += (key.shape[ax],)
      flatten_dim *= key.shape[ax]
    mask_shape += (flatten_dim,)

  def tri(n, m, k=0):
    # Tie in the key to avoid the mask becoming a constant.
    # This way XLA can construct the mask during computation and fuse it
    # with the attention ops.
    x = jnp.arange(n, dtype=jnp.int32)
    y = jnp.arange(m, dtype=jnp.int32)
    mask = lax.ge(
      (lax.broadcast_in_dim(x, shape=(n, m), broadcast_dimensions=(0,))) + k,
      lax.broadcast(y, [n]),
    )
    return mask

  k = -1 if self_mask else 0
  mask = tri(*mask_shape[-2:], k=k).reshape(mask_shape_final)
  return mask

