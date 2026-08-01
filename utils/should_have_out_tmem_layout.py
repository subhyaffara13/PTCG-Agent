
def should_have_out_tmem_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation results should be assigned a TMEM layout."""
  return any(
      isinstance(v.type, ir.MemRefType) and utils.is_tmem_ref(v)
      for v in op.results
  )

