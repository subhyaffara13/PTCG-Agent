
def _cast_to_bool(operand: Array) -> Array:
  if dtypes.issubdtype(operand.dtype, np.complexfloating):
    operand = operand.real
  return lax.convert_element_type(operand, np.bool_)

