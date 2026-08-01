
def _is_named_tuple(x):
  return (
      isinstance(x, tuple)
      and hasattr(x, "_fields")
      and hasattr(x, "__class__")
      and hasattr(x.__class__, "__name__")
  )

