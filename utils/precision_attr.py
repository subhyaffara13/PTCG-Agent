
def precision_attr(precision: Precision) -> ir.ArrayAttr:
  return ir.ArrayAttr.get(
      [hlo.PrecisionAttr.get(str(p)) for p in _full_precision(precision)]
  )

