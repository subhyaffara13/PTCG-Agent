
def _iota_staging_rule(trace, source_info, dtype, shape, dimension,
                       sharding):
  params = dict(dtype=dtype, shape=shape, dimension=dimension,
                sharding=sharding)
  return trace.default_process_primitive(iota_p, (), params,
                                           source_info=source_info)

