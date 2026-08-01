
def _convertible_to_int(p: Any) -> TypeGuard[SupportsIndex]:
  try:
    op.index(p)
    return True
  except:
    return False

