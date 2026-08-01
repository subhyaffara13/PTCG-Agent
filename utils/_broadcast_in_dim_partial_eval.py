
def _broadcast_in_dim_partial_eval(
    trace, operand, shape, broadcast_dimensions, sharding):
  return trace.default_process_primitive(
      broadcast_in_dim_p, (operand,),
      dict(shape=shape, broadcast_dimensions=broadcast_dimensions,
           sharding=sharding))

