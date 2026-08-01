
def _check_broadcast_shapes(name: str, shape: tuple | Shape | None, *args: ArrayLike):
  arg_shapes = [np.shape(a) for a in args]
  if shape is None:
    if arg_shapes:
      shape = lax.broadcast_shapes(*arg_shapes)
    else:
      shape = ()
  else:
    shape = core.canonicalize_shape(shape)
    _check_shape(name, shape, *arg_shapes)
  return shape

