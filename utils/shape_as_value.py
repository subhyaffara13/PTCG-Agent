
def shape_as_value(shape: core.Shape):
  """Converts a shape that may contain Poly values into a JAX value."""
  dtype = lax_utils.int_dtype_for_shape(shape, signed=True)
  if len(shape) == 0:
    return full((0,), np.array(0, dtype=dtype))
  if core.is_constant_shape(shape):
    return np.asarray(shape, dtype=dtype)
  dims = [
      expand_dims(convert_element_type(core.dimension_as_value(d), dtype),
                  (0,))
      for d in shape
  ]
  return concatenate(dims, dimension=0)

