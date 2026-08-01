
def any_axis_types_match(axis_types, ty: AxisType) -> bool:
  if not axis_types:
    return False
  return any(t == ty for t in axis_types)

