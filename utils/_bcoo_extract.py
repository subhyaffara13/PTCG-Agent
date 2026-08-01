
def _bcoo_extract(indices: Array, arr: Array, *, assume_unique=True) -> Array:
  """Extract BCOO data values from a dense array at given BCOO indices.

  Args:
    indices: An ndarray; see BCOO indices.
    arr: A dense array.
    assume_unique: bool, default=True
      If True, then indices will be assumed unique and a value will be extracted
      from arr for each index. Otherwise, extra work will be done to de-duplicate
      indices to zero-out duplicate extracted values.

  Returns:
    An ndarray; see BCOO data.
  """
  return bcoo_extract_p.bind(indices, arr, assume_unique=assume_unique)

