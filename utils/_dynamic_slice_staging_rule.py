
def _dynamic_slice_staging_rule(trace, source_info, x, *start_indices,
                                slice_sizes):
  return trace.default_process_primitive(
      dynamic_slice_p, (x, *start_indices), dict(slice_sizes=slice_sizes),
      source_info=source_info)

