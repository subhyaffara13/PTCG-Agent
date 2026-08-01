
def broadcasting_shape_rule(name, *avals, **kwargs):
  if not isinstance(name, str):
    raise RuntimeError(
      "First argument of broadcasting_shape_rule should be a name."
      f" Got {name}")
  shapes = [aval.shape for aval in avals if aval.shape]
  if not shapes:
    return ()
  return _try_broadcast_shapes(*shapes, name=name)

