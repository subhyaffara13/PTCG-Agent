
def _custom_primitive_op_results(flat_ret_ty) -> tuple[
    Sequence[ir.Type],
    Sequence[ir.Attribute | None],
]:
  """Returns a tuple containing the list of output MLIR types, and layouts for
  the given JAX return types."""
  results_ty: list[ir.Type] = []
  out_layouts: list[ir.Attribute | None] = []
  for r in flat_ret_ty:
    if not isinstance(r, ShapeDtypeStruct):
      raise NotImplementedError(f"Expected a ShapeDtypeStruct, but got: {r}")
    el_type = mgpu_utils.dtype_to_ir_type(r.dtype)
    if not r.shape:  # scalar case.
      results_ty.append(el_type)
      out_layouts.append(None)
    else:
      results_ty.append(ir.VectorType.get(r.shape, el_type))
      layout = mgpu_layouts.to_layout_attr(r.layout.to_mgpu())
      out_layouts.append(layout)
  return results_ty, out_layouts

