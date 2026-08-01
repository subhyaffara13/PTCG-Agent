
def _cast_to_shape(value, shape, dtype):
  """Casts `value` to the correct Python type for `shape` and `dtype`."""
  if shape is NUMPY_SCALAR_SHAPE:
    # explicitly cast to NumPy scalar in case `value` is a Python scalar.
    return np.dtype(dtype).type(value)
  elif shape is PYTHON_SCALAR_SHAPE:
    # explicitly cast to Python scalar via https://stackoverflow.com/a/11389998
    return np.asarray(value).item()
  elif type(shape) in (list, tuple):
    assert np.shape(value) == tuple(shape)
    return value
  elif np.ndim(shape) == 0:
    assert np.shape(value) == (shape,)
    return value
  else:
    raise TypeError(type(shape))

