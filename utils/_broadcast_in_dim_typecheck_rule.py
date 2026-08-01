
def _broadcast_in_dim_typecheck_rule(
    _, operand, shape, broadcast_dimensions, sharding):
  out_aval, effects = broadcast_in_dim_p.abstract_eval(
      operand.aval, shape=shape, broadcast_dimensions=broadcast_dimensions,
      sharding=sharding)
  return [out_aval], effects

