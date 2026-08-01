
def unwrap_statics(pytree, statics):
  if statics is False:
    return pytree
  elif statics is True:
    return pytree.val  # pytree should be a `Static` object
  elif isinstance(pytree, tuple):
    return tuple(unwrap_statics(p, s) for p, s in zip(pytree, statics))
  elif isinstance(pytree, dict):
    return {k : unwrap_statics(p, statics[k]) for k, p in pytree.items()}
  else:
    assert False, "unreachable"

