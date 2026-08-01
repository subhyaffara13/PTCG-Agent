
def _leaf_to_numpy(leaf: Any) -> np.ndarray:
  """Materialises a leaf to a contiguous numpy array for hashing.

  Multi-host jax.Arrays span devices the local process can't reach, so we
  hash only this process's addressable shards, concatenated in a stable
  (sorted-by-index) order — each host hashes the slice it owns.

  Args:
    leaf: A pytree leaf — a numpy array, a jax.Array, or a scalar.

  Returns:
    A contiguous numpy array of this process's addressable data.
  """
  if isinstance(leaf, np.ndarray):
    return np.ascontiguousarray(leaf)
  if hasattr(leaf, "addressable_shards"):
    shards = list(leaf.addressable_shards)
    if not shards:
      return np.ascontiguousarray(np.zeros((0,), dtype=np.float32))
    shards.sort(key=lambda s: tuple(s.index or ()))
    return np.ascontiguousarray(
        np.concatenate([np.asarray(s.data).ravel() for s in shards])
    )
  return np.ascontiguousarray(np.asarray(leaf))

