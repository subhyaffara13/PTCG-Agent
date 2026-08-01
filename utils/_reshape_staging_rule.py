
def _reshape_staging_rule(
    trace, source_info, x, new_sizes, dimensions, sharding):
  params = dict(new_sizes=new_sizes, dimensions=dimensions, sharding=sharding)
  return trace.default_process_primitive(reshape_p, (x,), params,
                                         source_info=source_info)

