
def preduced(x, axis_name):
  axes = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  if not axes:
    return x
  cur_mesh = get_abstract_mesh()
  if not config._check_vma.value and all(a in cur_mesh.manual_axes for a in axes):
    return x
  new_axes = axes if cur_mesh.empty else core.order_wrt_mesh(cur_mesh, axes)
  assert set(new_axes) == set(axes)
  del axes
  return tree_util.tree_map(lambda l: preduced_p.bind(l, axes=new_axes), x)

