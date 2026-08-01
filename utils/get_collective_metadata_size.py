
def get_collective_metadata_size(num_params: int, num_peers: int) -> int:
  """Returns the size of the collective metadata buffer for the given number of parameters and peers."""
  return (
      # Stores the collective metadata structure.
      COLLECTIVE_METADATA_SIZE
      # For each peer we need to store a pointer to each parameter.
      + num_peers * num_params
      # For each parameter we need to store a pointer to the multimem address.
      + num_params
  )

