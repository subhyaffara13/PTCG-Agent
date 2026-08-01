
def _stack_lowering_rule(ctx: LoweringRuleContext, *xs, axis):
  x_aval = ctx.avals_in[0]

  new_shape = list(x_aval.shape)
  new_shape.insert(axis, 1)

  new_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(tuple(new_shape)),
      _dtype_to_ir_type(x_aval.dtype)
  )

  if x_aval.shape:
    expanded_xs = [vector.shape_cast(new_type, x) for x in xs]
  else:
    expanded_xs = [vector.broadcast(new_type, x) for x in xs]
  if len(expanded_xs) == 1:
    return expanded_xs[0]
  return tpu.concatenate(expanded_xs, dimension=axis)


def _stack_lowering_rule(ctx: LoweringRuleContext, *args, axis):
  if len(args) != 2:
    raise NotImplementedError("Only 2-argument stack is supported in Triton.")
  [x_aval, y_aval] = ctx.avals_in
  x, y = args
  if axis != x_aval.ndim:
    raise NotImplementedError("Only stack along the last dimension is supported in Triton.")

  x = _ensure_ir_value(x, x_aval)
  y = _ensure_ir_value(y, y_aval)

  ty = ir.RankedTensorType(x.type)
  shape = list(ty.shape)
  shape.append(2)
  ret_type = ir.RankedTensorType.get(shape, ty.element_type, ty.encoding)

  return tt_dialect.join(ret_type, x, y)

