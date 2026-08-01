
def _reduce_precision_ur_rule(operand, *, exponent_bits, mantissa_bits):
  return core.getu(operand), core.getr(operand)

