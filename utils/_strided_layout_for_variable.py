
def _strided_layout_for_variable(
    variable: cs.Variable,
) -> fa.WGStridedFragLayout | None:
  """Returns a strided layout for the given variable.

  If the given variable cannot have a strided layout, returns `None`.
  """
  ty = variable.key.value.type
  assert isinstance(ty, ir.VectorType)
  return fa.WGStridedFragLayout.from_shaped_type(ty)

