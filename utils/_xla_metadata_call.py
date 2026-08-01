
def _xla_metadata_call(fun, **meta):
  def wrapped(*args, **kwargs):
    dbg = debug_info('xla_metadata_call', fun, args, kwargs)
    args_ft = FlatTree.flatten((args, kwargs))
    in_avals = args_ft.map(core.shaped_abstractify)
    jaxpr, out_avals = pe.trace_to_jaxpr(fun, in_avals, dbg)
    if any(isinstance(c, core.Tracer) for c in jaxpr.consts):
      jaxpr, consts = pe.separate_consts(jaxpr)
    else:
      consts = []
    outs_flat = xla_metadata_call_p.bind(*consts, *args_ft.vals, jaxpr=jaxpr,
                                         **meta)
    return tree_unflatten(out_avals.tree, outs_flat)
  return wrapped

