
def pvary(x, axis_name):
  axes = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  if not axis_name:
    return x
  cur_mesh = mesh_lib.get_abstract_mesh()
  if not config._check_vma.value and all(a in cur_mesh.manual_axes for a in axes):
    return x
  new_axes = axes if cur_mesh.empty else order_wrt_mesh(cur_mesh, axes)
  assert set(new_axes) == set(axes)
  del axes
  # TODO(yashkatariya): Remove this handling and remove_size_one_mesh_axis_from_type
  # generally from JAX.
  if config.remove_size_one_mesh_axis_from_type.value and not cur_mesh.empty:
    new_axes = tuple(i for i in new_axes if cur_mesh.shape[i] != 1)
    if not new_axes:
      return x
  return tree_map(lambda leaf: pvary_p.bind(leaf, axes=new_axes), x)

