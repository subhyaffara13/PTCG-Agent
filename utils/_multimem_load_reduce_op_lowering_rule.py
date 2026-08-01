
def _multimem_load_reduce_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.MultimemLoadReduceOp
) -> Sequence[ir.Value]:
  [out_layout_attr] = inference_utils.out_layouts(op)
  out_layout = layouts_lib.from_layout_attr(out_layout_attr)
  # TODO(apaszke): DO NOT IGNORE TRANSFORMS.

  assert ctx.launch_context is not None

  # pyrefly: ignore[missing-attribute]
  reduction = str(mgpu.MultimemLoadReductionType(op.reduction_type.value))
  if isinstance(op.source.type.element_type, ir.IntegerType):
    is_signed = reduction in ("smax", "smin")
    if reduction in ("smax", "smin", "umax", "umin"):
      reduction = reduction[1:]
  else:
    is_signed = None

  multimem_ref = utils.MultimemRef(op.source)
  fa_res = fa.FragmentedArray.load_reduce_untiled(
      multimem_ref,
      out_layout,  # pyrefly: ignore[bad-argument-type]
      reduction,  # pyrefly: ignore[bad-argument-type]
      is_signed=is_signed
  )

  return [fragmented_array_to_ir(fa_res, op.result.type)]

