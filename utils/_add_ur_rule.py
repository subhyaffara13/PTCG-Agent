
def _add_ur_rule(x, y):
  out_reduced = default_nary_reduced_rule(x, y)
  x_ur, y_ur = getu(x), getu(y)
  if x_ur and y_ur:
    if x_ur != y_ur:
      raise core.ShardingTypeError(
          'lhs and rhs to `add` must be unreduced along the same mesh axes. '
          f'Got lhs={x_ur}, rhs={y_ur}')
    out_unreduced = x_ur
  elif x_ur or y_ur:
    if x_ur and not y_ur:
      lhs_str, rhs_str = 'lhs', 'rhs'
    else:
      assert not x_ur and y_ur
      lhs_str, rhs_str = 'rhs', 'lhs'
    raise core.ShardingTypeError(
        f'{lhs_str} is unreduced while {rhs_str} is not. `add` operation does'
        ' not allow this because there will be implicit communication. Please'
        f' reduce {lhs_str} via `reshard` before calling `add`.')
  else:
    out_unreduced = frozenset()
  return out_unreduced, out_reduced

