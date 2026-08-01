
def _xla_metadata_call_transpose(cts_in, *primals_in, jaxpr, **meta):
  in_flat, in_tree = tree_flatten((primals_in, cts_in))
  in_avals = tuple(core.typeof(x) for x in in_flat)
  trans_jaxpr, out_tree = _transpose_jaxpr(jaxpr, in_avals, in_tree)
  cts_out = xla_metadata_call_p.bind(*in_flat, jaxpr=trans_jaxpr, **meta)
  return tree_unflatten(out_tree, cts_out)

