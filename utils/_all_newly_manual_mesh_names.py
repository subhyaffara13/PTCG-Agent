
def _all_newly_manual_mesh_names(
    mesh: BaseMesh, manual_axes: frozenset[AxisName]) -> tuple[AxisName, ...]:
  axis_env = core.get_axis_env()
  vmap_spmd_names = set(axis_env.spmd_axis_names)
  if not (ctx_mesh := get_abstract_mesh()).empty:
    mesh = ctx_mesh
    already_manual_names = set(ctx_mesh.manual_axes)
  else:
    # TODO(mattjj): remove this mechanism when we revise mesh scopes
    already_manual_names = set(axis_env.axis_sizes)  # may include vmap axis_names
  return tuple(name for name in mesh.axis_names
               if (name not in vmap_spmd_names | already_manual_names and
                   name in manual_axes))

