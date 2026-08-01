
def _num_programs_lowering_rule(ctx: LoweringRuleContext, *, axis: int):
  vmapped_axes = set(ctx.lowering_context.vmapped_dims)
  seen_user_axes = 0
  for i in range(ctx.lowering_context.grid_rank):
    seen_user_axes += int(i not in vmapped_axes)
    if seen_user_axes == axis + 1:
      break
  else:
    raise ValueError(
        f"user passed in program id with axis: {axis}, but grid only has"
        f" length: {ctx.lowering_context.grid_rank}"
    )
  return tpu.iteration_bound(i)


def _num_programs_lowering_rule(ctx: LoweringRuleContext, *, axis):
  if axis not in range(3):
    raise ValueError(f"axis must be in [0, 3), but got: {axis}")
  return tt_dialect.get_num_programs(axis)

