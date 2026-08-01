
def _reduce_precision_shape_rule(operand, *, exponent_bits, mantissa_bits):
  exponent_bits = operator.index(exponent_bits)
  mantissa_bits = operator.index(mantissa_bits)
  if exponent_bits < 1:
    raise ValueError(f"reduce_precision: exponent_bits must be positive; got {exponent_bits}")
  if mantissa_bits < 0:
    raise ValueError(f"reduce_precision: mantissa_bits must be non-negative; got {mantissa_bits}")
  return operand.shape

