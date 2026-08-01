
def keys_shaped_array(impl, shape, sharding, mat):
  aval = core.ShapedArray(shape, KeyTy(impl))
  return core.update_aval_with_sharding(aval, sharding, mat=mat)

