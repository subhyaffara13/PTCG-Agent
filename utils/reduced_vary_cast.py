
def reduced_vary_cast(x, axis_name):
  axes = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  if not axis_name:
    return x
  cur_mesh = mesh_lib.get_abstract_mesh()
  if not config._check_vma.value and all(a in cur_mesh.manual_axes for a in axes):
    return x
  new_axes = axes if cur_mesh.empty else order_wrt_mesh(cur_mesh, axes)
  assert set(new_axes) == set(axes)
  del axes
  return tree_map(lambda leaf: reduced_vary_cast_p.bind(leaf, axes=new_axes), x)

