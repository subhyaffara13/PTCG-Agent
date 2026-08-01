
def xla_metadata_call(f=None, **meta):
  if f is None:
    return lambda g: _xla_metadata_call(g, **meta)
  return _xla_metadata_call(f, **meta)

