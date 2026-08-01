
def is_valid_shape(shape, dtype):
  if shape == PYTHON_SCALAR_SHAPE:
    return dtype == np.dtype(type(np.array(0, dtype=dtype).item()))
  return True

