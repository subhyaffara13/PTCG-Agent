
def safe_to_summarize(array: jax.Array) -> bool:
  """Checks if the array is safe to summarize (not a tracer, not replicated)."""
  assert jax is not None, "JAX is not available."
  if isinstance(array, jax.core.Tracer):
    return False
  if array.is_deleted():
    return False
  if not _is_locally_available(array):
    return False
  thresh_dict = summarization_threshold.get()
  [platform] = set(device.platform for device in array.devices())
  thresh = thresh_dict.get(platform)
  if thresh is None:
    thresh = thresh_dict["default"]
  return thresh is None or array.size < thresh

