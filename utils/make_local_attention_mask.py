
def make_local_attention_mask(
    shape: tuple[int, int],
    window_size: tuple[int | None, int | None],
    *,
    offset: int = 0,
) -> np.ndarray:
  """Makes a local attention mask."""
  q_seq_len, kv_seq_len = shape
  q_idx = np.arange(q_seq_len, dtype=np.int32)
  kv_idx = np.arange(kv_seq_len, dtype=np.int32)
  mask = np.ones((q_seq_len, kv_seq_len), dtype=np.bool_)
  left, right = window_size
  if left is not None:
    mask = mask & (q_idx[:, None] - left + offset <= kv_idx[None, :])
  if right is not None:
    mask = mask & (q_idx[:, None] + right + offset >= kv_idx[None, :])
  return mask.astype(np.bool_)

