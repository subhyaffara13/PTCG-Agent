
def should_have_in_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation operands should be assigned a layout."""
  return any(isinstance(v.type, ir.VectorType) for v in op.operands)

