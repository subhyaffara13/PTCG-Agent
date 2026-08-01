
def _reshard_abstract_eval(aval, *, dst_sharding, concrete_mesh):
  assert isinstance(aval, core.ShapedArray)
  if aval.sharding == dst_sharding:
    return aval
  return aval.update(sharding=dst_sharding)

