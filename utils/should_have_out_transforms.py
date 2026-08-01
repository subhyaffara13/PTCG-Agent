
def should_have_out_transforms(op: ir.OpView) -> bool:
  """Returns 'True' if the operation should be assigned out transforms."""
  return any(map(is_transformable_smem_memref, op.results))

