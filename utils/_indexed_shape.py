
def _indexed_shape(ref: Ref, indices: Sequence[jax.Array]) -> tuple[int, ...]:
  if len(indices) != ref.ndim:
    raise ValueError(f"The number of indices does not match {ref.ndim=}")
  prev_idx: jax.Array | None = None
  for idx in indices:
    if idx.ndim != 1:
      raise ValueError(
          f"Indices must be a 1-D array, got an index with shape {idx.shape}"
      )
    if prev_idx is not None and idx.size != prev_idx.size:
      raise ValueError(
          "Indices must have the same size, got {prev_idx.size} and {idx.size}"
      )
    prev_idx = idx
  assert prev_idx is not None
  return (prev_idx.size,)

