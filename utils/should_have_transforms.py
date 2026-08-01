
def should_have_transforms(op: ir.OpView) -> bool:
  """Returns 'True' if the operation should be assigned in/out transforms."""
  return should_have_in_transforms(op) or should_have_out_transforms(op)

