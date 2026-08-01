
def _philox4x32_abstract_eval(*args):
  """Abstract evaluation rule for philox4x32_p."""
  if len(args) != 6:
    raise TypeError(f"philox4x32_p expects 6 arguments, got {len(args)}.")
  if all(isinstance(arg, core.ShapedArray) for arg in args):
    shape = lax.broadcasting_shape_rule("philox4x32", *args)
    sharding = lax.broadcasting_sharding_rule("philox4x32", *args)
    aval = core.ShapedArray(shape, np.dtype("uint32"), sharding=sharding)
  else:
    raise TypeError(f"Arguments to philox4x32 must all be arrays, got {args}")
  if any(a.dtype != np.uint32 for a in args):
    raise TypeError(
        f"Arguments to philox4x32 must have uint32 type, got {args}"
    )
  return (aval,) * 4

