
def make_chunk_attention_mask(
    shape: tuple[int, int], chunk_size: int
) -> np.ndarray:
  """Makes a chunked causal attention mask.

  Args:
    shape: The desired shape of the mask (q_seq_len, kv_seq_len).
    chunk_size: The size of the attention chunks.

  Returns:
    A boolean mask of shape `mask_shape` where True indicates attention is
    allowed according to chunked causal rules, and False otherwise.

  Raises:
    ValueError: If chunk_window_size is None or not positive.
  """
  if chunk_size <= 0:
    raise ValueError('chunk_size must be positive')

  q_seq_len, kv_seq_len = shape
  q_idx = np.arange(q_seq_len, dtype=np.int32)
  kv_idx = np.arange(kv_seq_len, dtype=np.int32)

  # chunk mask calculation
  same_chunk = (q_idx[:, None] // chunk_size) == (kv_idx[None, :] // chunk_size)
  mask = same_chunk & (q_idx[:, None] >= kv_idx[None, :])
  return mask

