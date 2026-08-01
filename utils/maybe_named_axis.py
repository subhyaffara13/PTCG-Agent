
def maybe_named_axis(axis, if_pos, if_named):
  try:
    pos = operator.index(axis)
  except TypeError:
    return if_named(axis)
  else:
    return if_pos(pos)

