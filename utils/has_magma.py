
def has_magma():
  if _cuhybrid:
    return _cuhybrid.has_magma()
  if _hiphybrid:
    return _hiphybrid.has_magma()
  return False

