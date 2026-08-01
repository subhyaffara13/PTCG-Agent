
def _iota_typecheck_rule(_, dtype, shape, dimension, sharding):
  out_aval, effects = iota_p.abstract_eval(
      dtype=dtype, shape=shape, dimension=dimension, sharding=sharding)
  return [out_aval], effects

