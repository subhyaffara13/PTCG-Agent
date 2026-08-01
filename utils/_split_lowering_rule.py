
def _split_lowering_rule(
    ctx: LoweringRuleContext, x, *, sizes, axis
):
  (x_aval,) = ctx.avals_in
  slice_size = np.array(x_aval.shape, dtype=np.int64)
  starts = np.zeros_like(slice_size)
  strides = np.ones_like(slice_size)
  outs = []
  for size, aval_out in zip(sizes, ctx.avals_out):
    slice_size[axis] = size
    outs.append(
        vector.extract_strided_slice(
            # pyrefly: ignore[bad-argument-type]
            ctx.aval_to_ir_type(aval_out), x, starts, slice_size, strides
        )
    )
    starts[axis] += size
  return outs


def _split_lowering_rule(ctx: LoweringRuleContext, x, *, sizes, axis):
  pass
  # TODO(cjfj): Add support for larger powers of 2.
  num_parts = len(sizes)
  if num_parts != pallas_utils.next_power_of_2(num_parts):
    raise NotImplementedError("Only power-of-2 num parts supported.")
  if any(size != sizes[0] for size in sizes):
    raise NotImplementedError("Only equal-sized splits are supported.")

  def split_into_2(x):
    shape = ir.RankedTensorType(x.type).shape
    x = _reshape(x, shape[:axis] + [2, shape[axis] // 2] + shape[axis + 1 :])
    permutation = tuple(d for d in range(len(shape) + 1) if d != axis) + (axis,)
    return tuple(tt_dialect.split(tt_dialect.trans(x, permutation)))

  x_parts: tuple[ir.Value, ...] = (x,)
  while len(x_parts) < num_parts:
    x_parts = sum(map(split_into_2, x_parts), ())
  return x_parts

