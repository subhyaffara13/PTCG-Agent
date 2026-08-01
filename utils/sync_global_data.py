
def sync_global_data(
    local_data: dict[str, Any],
) -> list[dict[str, Any]]:
  """Exchanges arbitrary JSON-serializable data with all hosts.

  Args:
    local_data: A dictionary of JSON-serializable data.

  Returns:
    A list of dictionaries containing the data from all hosts.
  """
  # 1. Serialize
  json_str = json.dumps(local_data)
  local_bytes = np.frombuffer(json_str.encode('utf-8'), dtype=np.uint8)
  local_len = jnp.array([len(local_bytes)], dtype=jnp.int32)

  # 2. Exchange Lengths
  all_lens = multihost_utils.process_allgather(local_len, tiled=False)
  max_len = int(jnp.max(all_lens))

  # 3. Pad to Max Length
  padded_bytes = np.zeros(max_len, dtype=np.uint8)
  padded_bytes[: len(local_bytes)] = local_bytes
  padded_bytes_jax = jnp.array(padded_bytes)

  # 4. Exchange Data
  all_padded_data = multihost_utils.process_allgather(
      padded_bytes_jax, tiled=False
  )

  # 5. Decode
  global_data = []
  all_padded_data_np = np.array(all_padded_data)
  # process_allgather with tiled=False concatenates results into a 1D array.
  # Reshape to (num_processes, max_len) for indexing.
  all_padded_data_np = all_padded_data_np.reshape(jax.process_count(), -1)

  for i in range(len(all_lens)):
    length = int(all_lens[i].item())
    valid_bytes = all_padded_data_np[i, :length]
    data_str = valid_bytes.tobytes().decode('utf-8')
    global_data.append(json.loads(data_str))

  return global_data

