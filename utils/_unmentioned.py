
def _unmentioned(mesh: Mesh | AbstractMesh, spec) -> list[AxisName]:
  vur = _spec_to_mat(spec).vur
  return [n for n in mesh.axis_names if n not in vur]

