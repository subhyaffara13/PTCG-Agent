
def _minmax_hlo(op, cmp, x, y):
  """Min/max that compares complex values lexicographically as pairs."""
  tensor_type = ir.RankedTensorType(x.type)
  if isinstance(tensor_type.element_type, ir.ComplexType):
    rx = hlo.real(x)
    ry = hlo.real(y)
    real_eq = compare_hlo(rx, ry, "EQ", "FLOAT")
    real_cmp = compare_hlo(rx, ry, cmp, "FLOAT")
    imag_cmp = compare_hlo(hlo.imag(x), hlo.imag(y), cmp, "FLOAT")
    which = hlo.select(real_eq, imag_cmp, real_cmp)
    return hlo.select(which, x, y)
  else:
    return op(x, y)

