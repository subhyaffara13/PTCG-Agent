
def mesh_local_to_global(mesh, axes: ArrayMapping, aval):
  return untile_aval_nd(mesh.shape, axes,
                        tile_aval_nd(mesh.local_mesh.shape, axes, aval))

