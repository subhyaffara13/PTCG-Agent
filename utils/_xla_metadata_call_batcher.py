
def _xla_metadata_call_batcher(axis_data, vals_in, dims_in, *, jaxpr, **meta):
  batched_jaxpr, dims_out = batching.batch_jaxpr2(jaxpr, axis_data, dims_in)
  outs = xla_metadata_call_p.bind(*vals_in, jaxpr=batched_jaxpr, **meta)
  return outs, dims_out

