
def chlo_precision_attr(precision: Precision) -> ir.ArrayAttr:
  return ir.ArrayAttr.get(
      [chlo.PrecisionAttr.get(str(p)) for p in _full_precision(precision)]
  )

