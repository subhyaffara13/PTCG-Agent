from typing import Any, Callable

def _unary_op_lowering_rule(
    _: LoweringContext,
    op: Any,
    impl: Callable[..., fa.FragmentedArray],
    is_signed: bool | None = None,
) -> Sequence[ir.Value]:
  in_layouts = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if any(in_layout != layout for in_layout in in_layouts):
    raise ValueError("Layout mismatch")
  a = _fragmented_array_from_ir(op.operand, layout, is_signed)
  if hasattr(op, "fastmath"):
    if op.fastmath == ir.Attribute.parse("#arith.fastmath<afn>"):
      result_fa = impl(a, approx=True)
    else:
      result_fa = impl(a)
  else:
    result_fa = impl(a)

  return [fragmented_array_to_ir(result_fa, op.result.type)]

