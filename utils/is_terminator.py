
def is_terminator(op: ir.OpView) -> bool:
  return isinstance(op, (scf.YieldOp, scf.ConditionOp))

