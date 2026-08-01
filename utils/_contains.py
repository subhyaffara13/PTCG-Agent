
def _contains(self: Array, other: ArrayLike) -> Array:
  """Implements __contains__ for JAX arrays.

  This is used by the Python ``in`` operator.
  """
  # Note: we deliberately depart from NumPy's behavior here, which includes
  # some oddities (https://github.com/numpy/numpy/issues/21933). Namely, we
  # require `self` to be a 1D array, and require `other` to be a scalar.'

  # Explicitly check for string and None types, as these were common bugs.
  if other is None or isinstance(other, str):
    raise TypeError(f"Array.__contains__: unsupported operand type {type(other)}.")
  query = util.ensure_arraylike('Array.__contains__', other)
  if self.ndim != 1:
    raise ValueError("Array.__contains__: search array must be one-dimensional,"
                     f" got arr.shape={self.shape}.")
  if query.ndim != 0:
    raise ValueError("Array.__contains__: query value must be a scalar,"
                     f" got {query.shape=}")
  return reductions.any(self == query)

