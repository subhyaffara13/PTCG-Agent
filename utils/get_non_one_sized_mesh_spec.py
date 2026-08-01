
def get_non_one_sized_mesh_spec(mesh, spec):
  spec = remove_size_one_mesh_axis(spec, mesh)
  axis_sizes, axis_names, axis_types = unzip3(
      [(s, n, t) for s, n, t in zip(mesh.axis_sizes, mesh.axis_names, mesh.axis_types)
      if s != 1])
  mesh = mesh_lib.AbstractMesh(axis_sizes, axis_names, axis_types)
  return mesh, spec

