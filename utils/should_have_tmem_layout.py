
def should_have_tmem_layout(op: MlirOperation) -> bool:
  """Returns 'true' if the operation should be assigned a TMEM layout."""
  return should_have_in_tmem_layout(op) or should_have_out_tmem_layout(op)

