
def _program_id_lowering_rule(ctx: LoweringRuleContext, *, axis: int):
  if ctx.lowering_context.user_grid_indices is None:
    raise ValueError(
        f"program id: {axis} was passed, but user did not provide a grid."
    )
  length = len(ctx.lowering_context.user_grid_indices)
  if axis not in range(length):
    raise ValueError(
        f"user passed in program id with axis: {axis}, but grid only has"
        f" length: {length}"
    )
  return ctx.lowering_context.user_grid_indices[axis]


def _program_id_lowering_rule(ctx: LoweringRuleContext, axis):
  if ctx.module_ctx.program_ids is None:
    raise NotImplementedError("pl.program_id() is not supported in this context")
  return ctx.module_ctx.program_ids[axis]


def _program_id_lowering_rule(ctx: LoweringRuleContext, *, axis):
  return ctx.context.program_ids[axis]

