
def _get_unique_sync_key() -> str | None:
  """Generate a thread-local key for ensuring all host finish (de)serializing"""
  if jax.process_count() == 1:
    return None
  # broadcast a thread-local unique barrier name
  sync_key_unique = multihost_utils.broadcast_one_to_all(
      np.frombuffer(uuid4().bytes, dtype=np.int32))
  sync_key_id = UUID(bytes=np.array(sync_key_unique).tobytes())
  return f"jax_sync_key_{str(sync_key_id)}"

