
def _threefry4x32_abstract_eval(*args):
  """Abstract evaluation for the threefry4x32 primitive."""
  if len(args) != 8:
    raise TypeError(f"threefry4x32_p expects 8 arguments, got {len(args)}.")
  if all(isinstance(arg, core.ShapedArray) for arg in args):
    shape = lax.broadcasting_shape_rule("threefry4x32", *args)
    sharding = lax.broadcasting_sharding_rule("threefry4x32", *args)
    aval = core.ShapedArray(shape, np.dtype("uint32"), sharding=sharding)
  else:
    raise TypeError(f"Arguments to threefry4x32 must all be arrays, got {args}")
  if any(a.dtype != np.uint32 for a in args):
    raise TypeError(
        f"Arguments to threefry4x32 must have uint32 type, got {args}"
    )
  return (aval,) * 4

