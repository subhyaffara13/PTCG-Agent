
def _target_op_to_attach_metadata(value_mlir: ir.Value) -> ir.Operation | None:
  op = value_mlir.owner
  if op is None or isinstance(op, ir.Block):
    return None
  return op.operation

