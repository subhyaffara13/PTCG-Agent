
def _is_custom_call(op: ir.Operation, name: str) -> TypeGuard[hlo.CustomCallOp]:
  return isinstance(op, hlo.CustomCallOp) and op.call_target_name.value == name

