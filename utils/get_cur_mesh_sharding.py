
def get_cur_mesh_sharding(spec=None):
  spec = P() if spec is None else spec
  return NamedSharding(mesh_lib.get_abstract_mesh(), spec)

