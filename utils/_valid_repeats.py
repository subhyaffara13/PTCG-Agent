
def _valid_repeats(mesh: Mesh, mat: core.ManualAxisType, spec) -> bool:
  um = set(_unmentioned(mesh, spec)) - set(mesh.manual_axes)
  vur = mat.vur
  if any(u in vur for u in um):
    return False
  return True

