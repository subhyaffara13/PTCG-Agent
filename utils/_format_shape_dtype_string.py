
def _format_shape_dtype_string(shape, dtype):
  if shape is NUMPY_SCALAR_SHAPE:
    return dtype_str(dtype)
  elif shape is PYTHON_SCALAR_SHAPE:
    return 'py' + dtype_str(dtype)
  elif type(shape) is tuple:
    shapestr = ','.join(str(dim) for dim in shape)
    return f'{dtype_str(dtype)}[{shapestr}]'
  elif type(shape) is int:
    return f'{dtype_str(dtype)}[{shape},]'
  else:
    raise TypeError(type(shape))

