
def _broadcast_in_dim_constraint_system(
    ctx: DerivationContext,
    op: mgpu.BroadcastInDimOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  src_variable = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  dst_variable = cs.Variable(ValueSite(op, VariableType.RESULT, 0))
  src_shape = tuple(op.operand.type.shape)
  dst_shape = tuple(op.result.type.shape)

  # Map destination index -> source index
  dst_to_src = {dst: src for src, dst in enumerate(op.broadcast_dimensions)}

  kept_dims = []
  collapsed_dims = []
  for dim in range(len(dst_shape)):
    if dim in dst_to_src:
      s_idx = dst_to_src[dim]
      # If the source was 1 but destination is > 1, we reduce but keep the dim.
      if src_shape[s_idx] == 1 and dst_shape[dim] > 1:
        kept_dims.append(dim)
    else:
      # If the dimension didn't exist in src_shape at all, we remove it.
      collapsed_dims.append(dim)

  assert kept_dims or collapsed_dims

  reduce_expr = dst_variable

  # 1. Apply keep_dims=True first. This keeps the rank the same,
  # so collapsed_dims indices remain valid.
  if kept_dims:
    reduce_expr = cs.Reduce(
        reduce_expr, axes=tuple(kept_dims), rank=len(dst_shape), keep_dims=True
    )

  # 2. Apply keep_dims=False to remove the added dimensions.
  if collapsed_dims:
    reduce_expr = cs.Reduce(
        reduce_expr, axes=tuple(collapsed_dims), rank=len(dst_shape), keep_dims=False
    )

  constraints = [
      # We need the `src = Reduce(...)` constraint to enforce correctness.
      # Alternatively, we could enforce it via the `IsSupportedBroadcast`
      # constraint but currently it doesn't do the necessary checks.
      cs.Equals(src_variable, reduce_expr),
      cs.IsSupportedBroadcast(
          src_variable, dst_variable, tuple(op.broadcast_dimensions)
      ),
  ]
  return (
      cs.ConstraintSystem(constraints=constraints),
      {
          src_variable: [src_variable.key],
          dst_variable: [dst_variable.key],
      },
  )

