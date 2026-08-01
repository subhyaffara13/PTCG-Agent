
def _is_logical_spec(x):
  return x is None or (
      isinstance(x, tuple) and all(_is_axis_spec(e) for e in x)
  )

