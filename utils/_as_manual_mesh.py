
def _as_manual_mesh(mesh, manual_axes: frozenset) -> AbstractMesh:
  return mesh.abstract_mesh.update_axis_types(
      {n: AxisType.Manual for n in manual_axes})

