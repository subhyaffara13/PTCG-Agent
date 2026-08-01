
def _closed_call_discharge_rule(
    in_avals: Sequence[core.AbstractValue], _,*args,
    call_jaxpr: core.ClosedJaxpr):
  discharged_closed_jaxpr, num_outs, fun = _cached_closed_jaxpr_discharge(call_jaxpr)
  out_and_ref_vals = core.closed_call_p.bind(*args, subfuns=(fun,),
                                             call_jaxpr=discharged_closed_jaxpr)
  out_vals, ref_vals = split_list(out_and_ref_vals, [num_outs])
  ref_vals_iter = iter(ref_vals)
  new_invals = tuple(next(ref_vals_iter) if isinstance(aval, AbstractRef)
                     else None for aval in in_avals)
  sentinel = object()
  assert next(ref_vals_iter, sentinel) is sentinel
  return new_invals, out_vals

