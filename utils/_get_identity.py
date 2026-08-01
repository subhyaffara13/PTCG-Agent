
def _get_identity(op, dtype):
  """Get an appropriate identity for a given operation in a given dtype."""
  if op is slicing.scatter_add:
    return 0
  elif op is slicing.scatter_mul:
    return 1
  elif op is slicing.scatter_min:
    if dtype == dtypes.bool_:
      return True
    elif dtypes.issubdtype(dtype, np.integer):
      return dtypes.iinfo(dtype).max
    return float('inf')
  elif op is slicing.scatter_max:
    if dtype == dtypes.bool_:
      return False
    elif dtypes.issubdtype(dtype, np.integer):
      return dtypes.iinfo(dtype).min
    return -float('inf')
  else:
    raise ValueError(f"Unrecognized op: {op}")

