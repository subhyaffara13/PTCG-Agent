
def _prepend_static_args(f, static_args, *args, **kwargs):
  static_args = tuple(arg.val for arg in static_args)
  all_args = static_args + args
  return f(*all_args, **kwargs)

