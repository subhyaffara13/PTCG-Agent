
def _promote_scalar_residuals_jaxpr(jaxpr: core.Jaxpr, which: Sequence[bool]):
  def fun(*res_and_args):
    res, args = split_list(res_and_args, [len(jaxpr.constvars)])
    res = [_rem_singleton(x) if w else x for x, w in zip(res, which)]
    return core.eval_jaxpr(jaxpr, res, *args)
  res_avals = [core.unmapped_aval(1, 0, v.aval) if w else v.aval
               for v, w in zip(jaxpr.constvars, which)]
  in_avals = FlatTree.flatten(((*res_avals, *[v.aval for v in jaxpr.invars]), {}))
  closed_jaxpr, _ = pe.trace_to_jaxpr(fun, in_avals, debug_info=jaxpr.debug_info)
  closed_jaxpr, _ = pe.separate_consts(closed_jaxpr)
  return closed_jaxpr.jaxpr

