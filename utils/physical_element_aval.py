
def physical_element_aval(edtype: dtypes.ExtendedDType) -> ShapedArray:
  duck = edtype._rules.physical_element_aval(edtype)
  return ShapedArray(duck.shape, dtypes.dtype(duck.dtype))

