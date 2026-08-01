
def _add_axis_to_metadata(fn, axis_pos, axis_name, axis_col='params_axes'):
  """Insert a named axis to axes metadata."""
  # Handle In() / Out() scan axis marker types.
  if hasattr(axis_pos, 'axis'):
    axis_pos = axis_pos.axis

  def insert_fn_leaf(names):
    if names is None:
      return names
    names = list(names)
    names.insert(axis_pos, axis_name)
    return tuple(names)

  def insert_fn(x):
    new_names = jax.tree_util.tree_map(
        insert_fn_leaf, x.names, is_leaf=_is_logical_spec
    )
    return x.replace(names=new_names)

  def remove_fn_leaf(names):
    if names is None:
      return names
    names = list(names)
    if names[axis_pos] != axis_name:
      raise ValueError(
          f'Expected axis {axis_name} at position {axis_pos} in '
          f'axis metadata {names}.'
      )
    names.pop(axis_pos)
    return tuple(names)

  def remove_fn(x):
    new_names = jax.tree_util.tree_map(
        remove_fn_leaf, x.names, is_leaf=_is_logical_spec
    )
    return x.replace(names=new_names)

  return nn.transforms.map_variables(
      fn,
      axis_col,
      mutable=_is_mutable(axis_col),
      trans_in_fn=lambda tree: _tree_map_axes(remove_fn, tree),
      trans_out_fn=lambda tree: _tree_map_axes(insert_fn, tree),
  )

