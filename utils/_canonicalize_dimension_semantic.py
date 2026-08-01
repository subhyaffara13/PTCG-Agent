
def _canonicalize_dimension_semantic(
    dimension_semantic: tpu_core.DimensionSemantics,
) -> tpu_core.LiteralDimensionSemantics:
  if isinstance(dimension_semantic, tpu_core.GridDimensionSemantics):
    return cast(tpu_core.LiteralDimensionSemantics, dimension_semantic.value)
  return dimension_semantic

