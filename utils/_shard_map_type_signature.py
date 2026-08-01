
def _shard_map_type_signature(eqn):
  return jaxpr_type_signature(eqn.params['jaxpr'])

