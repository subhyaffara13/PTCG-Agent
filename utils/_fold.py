
def _fold(x, fuel):
  if fuel <= 0:
    raise FoldingError()
  op_name = getattr(x.owner, "name", None)
  binop_folds = {
      "arith.maxsi": max,
      "arith.minsi": min,
  }
  if op_name == "arith.constant":
    if isinstance(x.type, ir.IntegerType):
      return ir.IntegerAttr(x.owner.attributes["value"]).value
    elif isinstance(x.type, ir.FloatType):
      return ir.FloatAttr(x.owner.attributes["value"]).value
    else:
      raise ValueError(f"Unsupported constant type: {x.type}")
  if op_name in binop_folds:
    return binop_folds[op_name](_fold(v, fuel - 1) for v in x.owner.operands)
  raise FoldingError()

