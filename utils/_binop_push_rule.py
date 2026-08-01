
def _binop_push_rule(
    prim: core.Primitive,
    ctx: PullRuleContext,
    left_block_spec: pallas_core.BlockSpec,
    right_block_spec: pallas_core.BlockSpec,
    **params: Any,
) -> pallas_core.BlockSpec | tuple[pallas_core.BlockSpec, ...]:
  del prim, params
  left_aval, right_aval = ctx.avals_in
  assert isinstance(left_aval, core.ShapedArray)
  assert isinstance(right_aval, core.ShapedArray)
  if not right_aval.shape:
    return left_block_spec
  if not left_aval.shape:
    return right_block_spec
  lhs_has_block_spec = left_block_spec is not pallas_core.no_block_spec
  rhs_has_block_spec = right_block_spec is not pallas_core.no_block_spec
  if not (lhs_has_block_spec ^ rhs_has_block_spec):
    # We can only do a push if one of the block specs is unspecified
    # or they are identical.
    if left_block_spec is right_block_spec:
      return left_block_spec
    raise ValueError('Illegal binary push. One of the block specs must be no_block_spec.')
  for l, r in zip(left_aval.shape, right_aval.shape, strict=True):
    if l == 1 and r != 1 and lhs_has_block_spec:
      raise ValueError('Cannot propagate block spec through LHS broadcast.')
    if r == 1 and l != 1 and rhs_has_block_spec:
      raise ValueError('Cannot propagate block spec through RHS broadcast.')
  if left_block_spec is pallas_core.no_block_spec:
    return right_block_spec
  if right_block_spec is pallas_core.no_block_spec:
    return left_block_spec
  if right_block_spec != left_block_spec:
    raise ValueError('Invalid block spec')
  return left_block_spec

