
def bcoo_extract(sparr: BCOO, arr: ArrayLike, *, assume_unique: bool | None = None) -> BCOO:
  """Extract values from a dense array according to the sparse array's indices.

  Args:
    sparr : BCOO array whose indices will be used for the output.
    arr : ArrayLike with shape equal to self.shape
    assume_unique : bool, defaults to sparr.unique_indices
      If True, extract values for every index, even if index contains duplicates.
      If False, duplicate indices will have their values summed and returned in
      the position of the first index.

  Returns:
    extracted : a BCOO array with the same sparsity pattern as self.
  """
  if not isinstance(sparr, BCOO):
    raise TypeError(f"First argument to bcoo_extract should be a BCOO array. Got {type(sparr)=}")
  a = jnp.asarray(arr)
  if a.shape != sparr.shape:
    raise ValueError(f"shape mismatch: {sparr.shape=} {a.shape=}")
  if assume_unique is None:
    assume_unique = sparr.unique_indices
  data = _bcoo_extract(sparr.indices, a, assume_unique=assume_unique)
  return BCOO((data, sparr.indices), **sparr._info._asdict())

