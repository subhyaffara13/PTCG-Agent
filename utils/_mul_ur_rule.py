
def _mul_ur_rule(x, y, *, out_dtype=None):
  del out_dtype  # unused
  out_reduced = default_nary_reduced_rule(x, y)
  x_ur, y_ur = getu(x), getu(y)
  if x_ur and y_ur:
    raise core.ShardingTypeError(
          'lhs and rhs to `mul` cannot be unreduced since mul is bilinear. '
          f'Got lhs={x_ur}, rhs={y_ur}')
  elif x_ur and not y_ur:
    if x_ur != getr(y):
      raise core.ShardingTypeError(
          'RHS should be reduced along the same axes LHS is unreduced on. Got'
          f' lhs={x} and rhs={y}')
    out_unreduced = x_ur
  elif not x_ur and y_ur:
    if getr(x) != y_ur:
      raise core.ShardingTypeError(
          'LHS should be reduced along the same axes RHS is unreduced on. Got'
          f' lhs={x} and rhs={y}')
    out_unreduced = y_ur
  else:
    assert not x_ur and not y_ur
    out_unreduced = frozenset()
  if out_unreduced:
    assert out_reduced == out_unreduced
    out_reduced = frozenset()  # if both are equal, set difference is empty.
  return out_unreduced, out_reduced

