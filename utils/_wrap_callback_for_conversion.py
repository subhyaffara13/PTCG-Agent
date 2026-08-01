
def _wrap_callback_for_conversion(
    callback: TrimmedStructureCallback[T],
    path: tuple[str | int, ...],
    original_key_by_clean_key: Mapping[str, str],
) -> TrimmedStructureCallback[T]:
  """Wraps callback to restore original keys in path after conversion."""
  t_len = len(path)

  def wrapped_callback(callback_path, val):
    clean_k = callback_path[t_len]
    orig_k = original_key_by_clean_key[clean_k]
    mapped_path = callback_path[:t_len] + (orig_k,) + callback_path[t_len + 1 :]
    callback(mapped_path, val)

  return wrapped_callback

