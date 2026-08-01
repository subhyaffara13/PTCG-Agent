
def _is_nan(x: ir.Value) -> ir.Value:
  return arith_dialect.cmpf(arith_dialect.CmpFPredicate.UNO, x, x)

