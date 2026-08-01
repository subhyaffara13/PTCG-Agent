
def should_have_in_tmem_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation operands should be assigned a TMEM layout."""
  return any(
      isinstance(v.type, ir.MemRefType) and utils.is_tmem_ref(v)
      for v in op.operands
  )

