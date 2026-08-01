
def prepend_static_args(f, static_args):
  return _prepend_static_args(f, tuple(Unhashable(arg) for arg in static_args))

