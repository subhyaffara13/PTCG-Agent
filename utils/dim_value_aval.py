
def dim_value_aval() -> AbstractValue:
  return ShapedArray((), dim_value_dtype(), weak_type=True, sharding=None)

