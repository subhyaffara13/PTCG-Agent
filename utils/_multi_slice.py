
def _multi_slice(self: Array,
                 start_indices: tuple[tuple[int, ...]],
                 limit_indices: tuple[tuple[int, ...]],
                 removed_dims: tuple[tuple[int, ...]]) -> list[Array]:
  """Extracts multiple slices from `arr`.

  This is used to shard Array arguments to pmap. It's implemented as a
  Array method here to avoid circular imports.
  """
  results: list[Array] = []
  for starts, limits, removed in zip(start_indices, limit_indices, removed_dims):
    sliced = lax_slicing.slice(self, starts, limits)
    if removed:
      sliced = lax.squeeze(sliced, removed)
    results.append(sliced)
  return results

