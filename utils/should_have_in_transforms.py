
def should_have_in_transforms(op: ir.OpView) -> bool:
  """Returns 'True' if the operation should be assigned in transforms."""
  return any(map(is_transformable_smem_memref, op.operands))

