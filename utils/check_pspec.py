
def check_pspec(mesh, spec, _manual_axes=frozenset()):
  _check_unique_resources(spec, "NamedSharding spec", mesh)
  _check_mesh_resource_axis(mesh, spec)
  _check_mesh_unreduced(mesh, spec)

