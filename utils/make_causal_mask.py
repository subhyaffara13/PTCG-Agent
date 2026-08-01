
def make_causal_mask(shape: tuple[int, int], offset: int = 0) -> np.ndarray:
  """Makes a causal attention mask.

  Args:
    shape: Shape of the 2-dim mask: (q_seq_len, kv_seq_len).
    offset: Offset of q start wrt kv. A positive offset shifts the bottom
      triangle upward, a negative one shifts it downward. A negative offset
      makes the first 'offset' rows of the attention matrix all 0s which leads
      to undefined softmax.

  Returns:
    The causal mask.
  """
  q_seq_len, kv_seq_len = shape
  q_idx = np.arange(q_seq_len, dtype=np.int32)
  kv_idx = np.arange(kv_seq_len, dtype=np.int32)
  return (q_idx[:, None] + offset >= kv_idx[None, :]).astype(np.bool_)


def make_causal_mask(
  x: Array, extra_batch_dims: int = 0, dtype: Dtype = jnp.float32
) -> Array:
  """Make a causal mask for self-attention.

  In case of 1d inputs (i.e., ``[batch..., len]``, the self-attention weights
  will be ``[batch..., heads, len, len]`` and this function will produce a
  causal mask of shape ``[batch..., 1, len, len]``.

  Args:
    x: input array of shape ``[batch..., len]``
    extra_batch_dims: number of batch dims to add singleton axes for, none by
      default
    dtype: mask return dtype

  Returns:
    A ``[batch..., 1, len, len]`` shaped causal mask for 1d attention.
  """
  idxs = jnp.broadcast_to(jnp.arange(x.shape[-1], dtype=jnp.int32), x.shape)
  return make_attention_mask(
    idxs,
    idxs,
    jnp.greater_equal,
    extra_batch_dims=extra_batch_dims,
    dtype=dtype,
  )


def make_causal_mask(
  x: Array, extra_batch_dims: int = 0, dtype: Dtype = jnp.float32
) -> Array:
  """Make a causal mask for self-attention.

  In case of 1d inputs (i.e., `[batch..., len]`, the self-attention weights
  will be `[batch..., heads, len, len]` and this function will produce a
  causal mask of shape `[batch..., 1, len, len]`.

  Args:
    x: input array of shape `[batch..., len]`
    extra_batch_dims: number of batch dims to add singleton axes for, none by
      default
    dtype: mask return dtype

  Returns:
    A `[batch..., 1, len, len]` shaped causal mask for 1d attention.
  """
  idxs = jnp.broadcast_to(jnp.arange(x.shape[-1], dtype=jnp.int32), x.shape)
  return make_attention_mask(
    idxs,
    idxs,
    jnp.greater_equal,
    extra_batch_dims=extra_batch_dims,
    dtype=dtype,
  )

