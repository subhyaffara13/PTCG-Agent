
def compare_hlo(x, y, direction: str, comparison_type: str | None = None):
  """Creates CompareOp."""
  if comparison_type is None:
    elem_type = ir.RankedTensorType(x.type).element_type
    if isinstance(elem_type, ir.IntegerType):
      comparison_type = "UNSIGNED" if elem_type.is_unsigned else "SIGNED"
    else:
      comparison_type = "FLOAT"

  return hlo.compare(
      x,
      y,
      hlo.ComparisonDirectionAttr.get(direction),
      compare_type=hlo.ComparisonTypeAttr.get(comparison_type))

