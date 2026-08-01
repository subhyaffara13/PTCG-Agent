
def _argnum_weak_type(*argnums):
  return lambda *args, **_: all(args[i].weak_type for i in argnums)

