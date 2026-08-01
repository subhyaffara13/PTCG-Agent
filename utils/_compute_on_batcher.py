
def _compute_on_batcher(axis_data, vals_in, dims_in, *, jaxpr, compute_type,
                        out_memory_spaces, compiler_options_json):
  batched_jaxpr, dims_out = batching.batch_jaxpr2(jaxpr, axis_data, dims_in)
  outs = compute_on_p.bind(*vals_in, jaxpr=batched_jaxpr,
                           compute_type=compute_type,
                           out_memory_spaces=out_memory_spaces,
                           compiler_options_json=compiler_options_json)
  return outs, dims_out

