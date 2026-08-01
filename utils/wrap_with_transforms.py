
def wrap_with_transforms(f, transforms, *args):
  new_args = tuple(
      state_types.TransformedRef(a, t) if t else a
      for a, t in zip(args, transforms)
  )
  return f(*new_args)

