
def _broadcast_in_dim_staging_rule(
    trace, source_info, x, shape, broadcast_dimensions, sharding):
  params = dict(shape=shape, broadcast_dimensions=broadcast_dimensions,
                sharding=sharding)
  return trace.default_process_primitive(broadcast_in_dim_p, (x,), params,
                                         source_info=source_info)

