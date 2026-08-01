
def _is_str_same_on_all_hosts(path: str | PathLike[str]) -> bool:
  """All-gather the location of the checkpoint and check if it's the same."""
  if jax.process_count() <= 1:
    return False
  path_b = str(path).encode("utf-8")
  if len(path_b) > _MAX_PATH_LENGTH:
    raise ValueError(f"Path exceeds maximum length of {_MAX_PATH_LENGTH} in"
                     " multiprocess case.")
  path_array = np.concatenate([
      np.frombuffer(path_b, dtype=np.uint8), np.zeros(
          _MAX_PATH_LENGTH - len(path_b), dtype=np.uint8)])
  path_array = multihost_utils.process_allgather(path_array)
  return bool(np.all(path_array[0] == path_array[1:]))

