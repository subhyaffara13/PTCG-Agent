
def _is_triton_pointer_type(t):
  if hasattr(tt_dialect.PointerType, "isinstance"):
    return tt_dialect.PointerType.isinstance(t)
  return isinstance(t, tt_dialect.PointerType)

