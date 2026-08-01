
def should_have_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation should be assigned a layout."""
  return should_have_in_layout(op) or should_have_out_layout(op)

