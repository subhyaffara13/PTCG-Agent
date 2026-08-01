
def _cmp(name, column_set):
    return any(all(a == b for a, b in zip(name, _)) for _ in column_set)


def _cmp(
    x: ir.Value,
    y: ir.Value,
    si_pred: arith_dialect.CmpIPredicate,
    ui_pred: arith_dialect.CmpIPredicate,
    f_pred: arith_dialect.CmpFPredicate,
    *,
    signed: bool,
) -> ir.Value:
  assert x.type == y.type, (str(x.type), str(y.type))
  x_element_type = _element_type(x.type)
  if isinstance(x_element_type, ir.IntegerType):
    return arith_dialect.cmpi(si_pred if signed else ui_pred, x, y)
  elif isinstance(x_element_type, ir.FloatType):
    return arith_dialect.cmpf(f_pred, x, y)
  else:
    raise NotImplementedError(f"unsupported types: {x.type} and {y.type}")

