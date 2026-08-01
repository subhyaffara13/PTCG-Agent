
def _flatten_ir_values(
    values: Sequence[ir.Value], fa_layouts: Iterable[ir.Attribute]
) -> tuple[Sequence[ir.Value], Sequence[_VectorTemplate | None]]:
  """Flattens a sequence of values.

  Non-vector values are preserved as is. Vectors are mapped to fragmented
  arrays and then flattened into per-register values.

  Args:
    values: The sequence of values to flatten.
    fa_layouts: The layouts of vectors in ``values``.

  Returns:
    A tuple of (flattened values, templates). The templates are used to
    reconstruct the vectors from the per-register  values.
  """
  fa_layouts_it = iter(fa_layouts)
  result: list[ir.Value] = []
  templates: list[_VectorTemplate | None] = []
  for v in values:
    if isinstance(v.type, ir.VectorType):
      arr = _fragmented_array_from_ir(v, next(fa_layouts_it))
      result.extend(arr.registers.flat)
      templates.append((arr.registers.shape, arr.layout, ir.VectorType(v.type)))
    else:
      result.append(v)
      templates.append(None)
  return result, templates

