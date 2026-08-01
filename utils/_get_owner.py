
def _get_owner(v):
  if isinstance(v, ir.Operation):
    return v
  if isinstance(v, ir.BlockArgument):
    return v.owner
  owner = v.owner
  op = owner.operation if isinstance(owner, ir.OpView) else owner
  while op.name == "sdy.sharding_constraint":
    v = op.operands[0]
    return _get_owner(v)
  return op

