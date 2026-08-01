
def mesh_global_to_local(mesh, axes: ArrayMapping, aval):
  return untile_aval_nd(mesh.local_mesh.shape, axes,
                        tile_aval_nd(mesh.shape, axes, aval))

