from typing import Any

def _divf_lowering_rule(
    ctx: LoweringContext, op: Any
) -> Sequence[ir.Value]:
  [layout] = inference_utils.out_layouts(op)
  lhs_ty = ir.VectorType(op.lhs.type)
  if isinstance(lhs_ty.element_type, ir.Float8E8M0FNUType):
    lhs_layout = layouts_lib.from_layout_attr(
        op.lhs.owner.attributes["layout"]
    )
    if isinstance(lhs_layout, fa.WGSplatFragLayout):
      [source] = op.lhs.owner.opview.operands
      if (
          isinstance(source.owner.opview, arith.ConstantOp)
          and float(ir.FloatAttr(source.owner.opview.value)) == 1.0
      ):
        rhs = _fragmented_array_from_ir(op.rhs, layout)
        return [fragmented_array_to_ir(1 / rhs, op.result.type)]
  return _binary_op_lowering_rule(
      ctx, op, is_signed=None, impl=operator.truediv
  )

