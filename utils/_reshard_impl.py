
def _reshard_impl(x, *, dst_sharding, concrete_mesh):
  thunk = lambda: dispatch.apply_primitive(
      reshard_p, x, dst_sharding=dst_sharding, concrete_mesh=concrete_mesh)
  if concrete_mesh is None:
    return thunk()
  else:
    with sharding_impls.set_mesh(concrete_mesh):
      return thunk()

