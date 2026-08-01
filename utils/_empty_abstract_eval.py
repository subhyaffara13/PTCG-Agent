
def _empty_abstract_eval(*, shape, dtype, out_sharding):
  return core.ShapedArray(shape, dtype, sharding=out_sharding)

