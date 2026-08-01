
def _get_carry_argnum(axes, is_in_axes: bool):
  if axes is Carry:
    return 'all'
  elif isinstance(axes, int) or axes is None:
    return None

  obj_repr = 'in_axes' if is_in_axes else 'out_axes'
  carry_argnum: int | None = None
  prev_key: tp.Any = None
  for key, x in jax.tree_util.tree_leaves_with_path(axes):
    if x is not Carry:
      continue
    assert isinstance(key[0], jax.tree_util.SequenceKey)
    i = key[0].idx
    if len(key) >= 2:
      raise ValueError(
        f'Carry must at the top-level, it cannot be nested. Found {axes=}'
      )
    if carry_argnum is not None:
      raise ValueError(
        f'Found multiple Carry definitions at '
        f'{obj_repr}{jax.tree_util.keystr(prev_key)} and '
        f'{obj_repr}{jax.tree_util.keystr(key)}'
      )
    carry_argnum = i
    prev_key = key

  return carry_argnum

