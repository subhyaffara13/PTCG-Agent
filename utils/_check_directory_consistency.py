
def _check_directory_consistency(directory: path_types.PathLike):
  """Raises error if directory paths are not consistent across processes.

  Args:
    directory: The directory path to check.

  Raises:
    ValueError: If the directory paths are not consistent across processes.
  """
  if multihost.process_count() <= 1:
    return

  path_str = str(directory)
  path_hash = hashlib.sha256(path_str.encode('utf-8')).digest()
  path_hash_arr = np.frombuffer(path_hash, dtype=np.uint8)

  # Broadcast the path hash from process 0 to all other processes.
  broadcasted_hash_arr = multihost.broadcast_one_to_all(path_hash_arr)

  # Gather mismatch status from all processes.
  mismatch_detected = np.array(
      0 if np.array_equal(path_hash_arr, broadcasted_hash_arr) else 1,
      dtype=np.int32,
  )
  all_mismatches = multihost.process_allgather(mismatch_detected)
  total_mismatches = np.sum(np.array(all_mismatches))

  if total_mismatches > 0:
    raise ValueError(
        'Directory path mismatch in multi-process save. '
        f"Process {jax.process_index()} has path '{path_str}'. (See logs from "
        'other processes for their paths.) Ensure all JAX processes are saving '
        'to the exact same directory path. If using create_tempdir in tests, '
        "provide the 'name' argument to ensure all processes generate the same "
        'path.'
    )

