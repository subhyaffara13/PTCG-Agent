
def _validate_scan_axes(in_axes, out_axes):
  is_axis_leaf = lambda x: x is None or x is Carry

  in_carry_count = 0
  for path, leaf in jax.tree_util.tree_leaves_with_path(
      in_axes, is_leaf=is_axis_leaf
  ):
    if leaf is Carry:
      in_carry_count += 1
      if len(path) > 1:
        raise ValueError(
            'Carry must be a top-level argument, it cannot be nested. '
            f'Found Carry inside in_axes at path {jax.tree_util.keystr(path)}'
        )
  if in_carry_count > 1:
    raise ValueError('Found multiple Carry definitions in in_axes')

  out_carry_count = 0
  for path, leaf in jax.tree_util.tree_leaves_with_path(
      out_axes, is_leaf=is_axis_leaf
  ):
    if leaf is Carry:
      out_carry_count += 1
      if len(path) > 1:
        raise ValueError(
            'Carry must be a top-level argument, it cannot be nested. '
            f'Found Carry inside out_axes at path {jax.tree_util.keystr(path)}'
        )
  if out_carry_count > 1:
    raise ValueError('Found multiple Carry definitions in out_axes')

  in_has_carry = in_carry_count > 0
  out_has_carry = out_carry_count > 0
  if in_has_carry != out_has_carry:
    raise ValueError(
        'If one of in_axes or out_axes has Carry, the other must also '
        f'have Carry. Got {in_axes=}, {out_axes=}'
    )

