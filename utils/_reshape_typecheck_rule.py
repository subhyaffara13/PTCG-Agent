
def _reshape_typecheck_rule(_, operand, new_sizes, dimensions,
                            sharding):
  out_aval, effects = reshape_p.abstract_eval(
      operand.aval, new_sizes=new_sizes, dimensions=dimensions,
      sharding=sharding)
  return [out_aval], effects

