
def _fused_batcher(axis_data, vals_in, dims_in, *, jaxpr, out_spaces):
  batched_jaxpr, dims_out = batching.batch_jaxpr2(jaxpr, axis_data, dims_in)
  outs = fused_p.bind(*vals_in, jaxpr=batched_jaxpr, out_spaces=out_spaces)
  return outs, dims_out

