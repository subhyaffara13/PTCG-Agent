
def _all_mesh_names_except_spmd(
    mesh: Mesh, manual_axes: frozenset[AxisName]) -> tuple[AxisName, ...]:
  axis_env = core.get_axis_env()
  spmd_names = axis_env.spmd_axis_names
  return tuple(name for name in mesh.axis_names
               if name not in spmd_names and name in manual_axes)

