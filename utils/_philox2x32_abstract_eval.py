
def _philox2x32_abstract_eval(*args):
  """Abstract evaluation rule for philox2x32_p."""
  if len(args) != 3:
    raise TypeError(f"philox2x32_p expects 3 arguments, got {len(args)}.")
  if all(isinstance(arg, core.ShapedArray) for arg in args):
    shape = lax.broadcasting_shape_rule("philox2x32", *args)
    sharding = lax.broadcasting_sharding_rule("philox2x32", *args)
    aval = core.ShapedArray(shape, np.dtype("uint32"), sharding=sharding)
  else:
    raise TypeError(f"Arguments to philox2x32 must all be arrays, got {args}")
  if any(a.dtype != np.uint32 for a in args):
    raise TypeError(
        f"Arguments to philox2x32 must have uint32 type, got {args}"
    )
  return (aval,) * 2

