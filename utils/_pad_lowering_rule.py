
def _pad_lowering_rule(ctx: LoweringRuleContext, *args, **kwargs):
  operand, padding_value = args
  padding_config = kwargs["padding_config"]

  out_type = ctx.aval_to_ir_type(ctx.avals_in[0])
  if not isinstance(out_type, ir.VectorType):
    raise NotImplementedError("Only vector types are supported.")

  for axis, (low, high, interior) in enumerate(padding_config):
    if low == 0 and high == 0 and interior == 0:
      continue

    def _pad(val, axis=axis):
      assert isinstance(operand.type, ir.VectorType)
      shape = list(operand.type.shape)
      shape[axis] = val
      pad_vec_type = ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(tuple(shape)),
          operand.type.element_type,
      )

      if isinstance(padding_value, ir.Value):
        pad = vector.broadcast(pad_vec_type, padding_value)
      else:
        scalar_attr = ir.FloatAttr.get(operand.type.element_type, padding_value)
        pad = arith.constant(
            pad_vec_type,
            ir.DenseElementsAttr.get_splat(pad_vec_type, scalar_attr),
        )
      return pad

    if low != 0:
      operand = tpu.concatenate([_pad(low), operand], dimension=axis)

    if high != 0:
      operand = tpu.concatenate([operand, _pad(high)], dimension=axis)

    if interior > 0:
      raise NotImplementedError("Not implemented: interior padding")

  return operand

