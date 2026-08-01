
def physical_shape(logical_shape, dtype):
  elt_aval = physical_element_aval(dtype)
  return (*logical_shape, *elt_aval.shape)

