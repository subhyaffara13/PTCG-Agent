
def check_unreduced_constraint(op: ir.Value | ir.Operation, aval) -> None:
  if not isinstance(aval, core.ShapedArray):
    return
  if not aval.sharding.spec.unreduced:
    return
  if isinstance(op, ir.Value):
    op = op.owner.operation if isinstance(op.owner, ir.OpView) else op.owner  # type: ignore
  assert isinstance(op, ir.Operation)
  if op.name in ("func.call", "sdy.manual_computation", "mpmd.named_computation"):
    return
  assert op.name == "sdy.sharding_constraint", (
      f"Expected last op to be sdy.sharding_constraint, but got: {op.name} and "
      f"output type={aval.str_short(True)}")
  sharding = sdy.TensorShardingAttr(op.attributes["sharding"])
  assert sharding.unreduced_axes, (
      "Expected sdy.sharding_constraint to have unreduced_axes populated, "
      f"but got: {sharding} and output type={aval.str_short(True)}")

