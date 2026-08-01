
def _binary_op_lowering_rule(ctx: LoweringRuleContext, x, y, *, impl, out_dtype=None):
  del out_dtype  # unused here.
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if not all(aval_in.shape == () for aval_in in ctx.avals_in):
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  x, y = _bcast(x, y, *ctx.avals_in, *ctx.avals_out)
  return impl(x, y)


def _binary_op_lowering_rule(
    _: LoweringContext,
    op: Any,
    is_signed: bool | None,
    impl: Callable[
        [fa.FragmentedArray, fa.FragmentedArray], fa.FragmentedArray
    ],
) -> Sequence[ir.Value]:
  in_layouts = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if any(in_layout != layout for in_layout in in_layouts):
    raise ValueError("Layout mismatch")
  lhs = _fragmented_array_from_ir(op.lhs, layout, is_signed)
  rhs = _fragmented_array_from_ir(op.rhs, layout, is_signed)
  return [fragmented_array_to_ir(impl(lhs, rhs), op.result.type)]

