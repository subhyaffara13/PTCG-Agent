
def _arith_constant_op_lowering_rule(
    _: LoweringContext, op: arith.ConstantOp
) -> Sequence[ir.Value]:
  if not isinstance(op.value, ir.DenseElementsAttr):
    raise NotImplementedError(f"Unsupported constant op: {op}")

  value = ir.DenseElementsAttr(op.value)
  if not value.is_splat:
    raise NotImplementedError(f"Unsupported constant op: {op}")

  ty = ir.VectorType(op.result.type)
  is_signed = _default_is_signed(ty.element_type)
  layout = layouts_lib.from_layout_attr(inference_utils.out_layouts(op)[0])
  return [
      fragmented_array_to_ir(
          fa.FragmentedArray.splat(
              arith.constant(ty.element_type, value.get_splat_value()),
              tuple(ty.shape),
              layout,
              is_signed=is_signed,
          ),
          op.result.type,
      )
  ]

