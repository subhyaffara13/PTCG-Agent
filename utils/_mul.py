
def _mul(scalar, tree):
  return tree_map(partial(operator.mul, scalar), tree)


def _mul(x: ir.Value, y: ir.Value, *, out_dtype=None) -> ir.Value:
  if out_dtype is not None:
    raise NotImplementedError("out_dtype is not supported..")
  assert x.type == y.type, (str(x.type), str(y.type))
  x_element_type = _element_type(x.type)
  if isinstance(x_element_type, ir.IntegerType):
    return arith_dialect.muli(x, y)
  elif isinstance(x_element_type, ir.FloatType):
    return arith_dialect.mulf(x, y)
  raise NotImplementedError(f"unsupported types: {x.type} and {y.type}")

