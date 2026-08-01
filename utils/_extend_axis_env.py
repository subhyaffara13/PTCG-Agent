
def _extend_axis_env(mesh, newly_manual_axes):
  all_manual_axes = newly_manual_axes | set(mesh.manual_axes)
  return core.extend_axis_env_nd([(k, v) for k, v in mesh.shape.items()
                                  if k in all_manual_axes])

