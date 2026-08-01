
def _maybe_skip_one_sized_axes(axes):
  if config.remove_size_one_mesh_axis_from_type.value:
    cur_mesh = get_abstract_mesh()
    return tuple(i for i in axes
                 if (size := cur_mesh.shape.get(i)) is None or size != 1)
  return axes

