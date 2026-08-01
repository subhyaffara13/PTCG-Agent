
def _threefry2x32_abstract_eval(*args):
  if any(a.dtype != np.uint32 for a in args):
    raise TypeError("Arguments to threefry2x32 must have uint32 type, got {}"
                    .format(args))
  if all(isinstance(arg, core.ShapedArray) for arg in args):
    shape = lax.broadcasting_shape_rule("threefry2x32", *args)
    sharding = lax.broadcasting_sharding_rule("threefry2x32", *args)
    aval = core.ShapedArray(shape, np.dtype('uint32'), sharding=sharding)
  else:
    raise TypeError(f"Arguments to threefry2x32 must all be arrays, got {args}")
  return (aval,) * 2

