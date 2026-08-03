from typing import Any

def as_abstract_type(value) -> Any:
  """Converts a value to its abstract type."""

  if isinstance(value, jax.Array):
    return abstract_arrays.to_shape_dtype_struct(value)
  elif isinstance(value, np.ndarray):
    return numpy_leaf_handler.NumpyShapeDtype(value.shape, value.dtype)
  elif isinstance(value, int):
    return int
  elif isinstance(value, float):
    return float
  elif isinstance(value, np.number):
    return value.dtype.type
  elif isinstance(value, str):
    return str
  else:
    raise ValueError(f'Unsupported type: {type(value)}')

