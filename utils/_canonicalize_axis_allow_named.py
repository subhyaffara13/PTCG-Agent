
def _canonicalize_axis_allow_named(x, rank):
  return maybe_named_axis(x, lambda i: canonicalize_axis(i, rank), lambda name: name)

