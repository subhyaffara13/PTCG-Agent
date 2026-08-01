
def _all_to_all_is_async(x, axis_name, split_axis, concat_axis, *,
                         axis_index_groups=None, tiled=False, is_async=False):
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  def bind(x, split_axis=split_axis, concat_axis=concat_axis):
    group_size = _axis_size(axis_name, axis_index_groups)
    if tiled:
      if x.shape[split_axis] % group_size != 0:
        raise ValueError(f"The size of all_to_all split_axis ({x.shape[split_axis]}) "
                         f"has to be divisible by the size of the named axis "
                         f"{axis_name} ({group_size})")
    else:
      if group_size != x.shape[split_axis]:
        msg = ("all_to_all requires the size of the mapped axis axis_name to "
               "equal x.shape[split_axis], but they are {} and {} respectively.")
        raise ValueError(msg.format(group_size, x.shape[split_axis]))
      if split_axis < concat_axis:
        concat_axis += 1  # concat_axis gives a position _after_ split_axis is removed
        x = lax.expand_dims(x, (concat_axis,))  # insert the new axis
      elif split_axis == concat_axis:
        pass
      else:  # concat_axis < split_axis
        x = lax.expand_dims(x, (concat_axis,))  # insert the new axis
        split_axis += 1   # we have a new axis before split_axis now
    x = insert_collective_pvary(axis_name, x)
    prim = all_to_all_start_p if is_async else all_to_all_p
    result = prim.bind(x, split_axis=split_axis, concat_axis=concat_axis,
                               axis_name=axis_name,
                               axis_index_groups=axis_index_groups,
                               tiled=tiled)
    if not tiled and split_axis != concat_axis:
      result = lax.squeeze(result, (split_axis,))
    return result

  return tree_util.tree_map(bind, x)

