
def should_have_out_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation results should be assigned a layout."""
  return any(isinstance(v.type, ir.VectorType) for v in op.results)

