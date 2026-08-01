
def _infer_flat_result_types(
    op: ir.OpView, out_layouts: Sequence[ir.Attribute]
) -> Sequence[ir.Type]:
  result_types: list[ir.Type] = []
  out_layouts_it = iter(out_layouts)
  for r in op.results:
    if not isinstance(r.type, ir.VectorType):
      result_types.append(r.type)
      continue
    vec_type = ir.VectorType(r.type)
    layout = layouts_lib.from_layout_attr(next(out_layouts_it))
    reg_type: ir.Type = layout.registers_element_type(vec_type.element_type)
    result_types.extend(
        [reg_type] * math.prod(layout.registers_shape(tuple(vec_type.shape)))
    )
  return result_types

