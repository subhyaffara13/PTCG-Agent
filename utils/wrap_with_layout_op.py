
def wrap_with_layout_op(ctx: LoweringRuleContext,
                        x: ir.Value,
                        aval_out: core.AbstractValue,
                        layout: Layout,
                        aval_in: core.AbstractValue):
  (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
  out_shape = core.physical_aval(aval_out).shape  # pyrefly: ignore[missing-attribute]
  if core.is_constant_shape(out_shape):
    result_shapes = None
  else:
    result_shapes = [eval_dynamic_shape_as_tensor(ctx, out_shape)]

  op = custom_call('LayoutConstraint', result_types=[result_type], operands=[x],
                   api_version=1,
                   result_shapes=result_shapes,
                   # Set operand layouts to anything. XLA will ignore it.
                   operand_layouts=[list(range(aval_in.ndim))],  # pyrefly: ignore[missing-attribute]
                   # TODO(yashkatariya): Figure out how to pass tiling to the
                   # custom call.
                   result_layouts=[layout.major_to_minor[::-1]])
  return op.result

