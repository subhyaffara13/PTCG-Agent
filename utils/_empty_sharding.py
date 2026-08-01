
def _empty_sharding(ndim):
  return NamedSharding(mesh_lib.empty_abstract_mesh, P(*[None] * ndim))

