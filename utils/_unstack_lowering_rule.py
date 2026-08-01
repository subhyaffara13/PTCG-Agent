
def _unstack_lowering_rule(ctx: LoweringRuleContext, x, *, axis):
  (x_aval,) = ctx.avals_in

  slice_size = list(x_aval.shape)
  starts = [0] * len(slice_size)
  strides = [1] * len(slice_size)

  (out_aval_example,) = ctx.avals_out[:1]
  out_type = ctx.aval_to_ir_type(out_aval_example)

  outs = []
  for i in range(x_aval.shape[axis]):
    starts[axis] = i
    slice_size[axis] = 1

    sliced_shape = list(x_aval.shape)
    sliced_shape[axis] = 1
    sliced_type = ir.VectorType.get(
        ctx.lowering_context.dynamic_shape_replacement_fn(tuple(sliced_shape)),
        _dtype_to_ir_type(x_aval.dtype)
    )

    slice_val = vector.extract_strided_slice(
        sliced_type, x, starts, slice_size, strides
    )
    if out_aval_example.shape:
      outs.append(vector.shape_cast(out_type, slice_val))
    else:
      outs.append(vector.extract(slice_val, [], [0]))

  return outs


def _unstack_lowering_rule(ctx: LoweringRuleContext, x, *, axis):
  [x_aval] = ctx.avals_in
  if x_aval.shape[axis] != 2:
    raise NotImplementedError("Only unstack of size 2 is supported in Triton.")
  if axis != x_aval.ndim - 1:
    raise NotImplementedError("Only unstack along the last dimension is supported in Triton.")

  x = _ensure_ir_value(x, x_aval)
  return tuple(tt_dialect.split(x))

