
def _call_primitive_discharge_rule(
    prim: core.Primitive,
    in_avals: Sequence[core.AbstractValue], _,*args,
    call_jaxpr: core.Jaxpr, **kwargs):
  closed_call_jaxpr = core.ClosedJaxpr(call_jaxpr, ())
  discharged_closed_jaxpr, num_outs, fun = _cached_closed_jaxpr_discharge(
      closed_call_jaxpr)
  discharged_call_jaxpr = discharged_closed_jaxpr.jaxpr
  discharged_consts = discharged_closed_jaxpr.consts
  discharged_call_jaxpr = pe.convert_constvars_jaxpr(discharged_call_jaxpr)
  out_and_ref_vals = prim.bind(
      *discharged_consts,
      *args,
      subfuns=(fun,),
      call_jaxpr=discharged_call_jaxpr,
      **kwargs,
  )
  out_vals, ref_vals = split_list(out_and_ref_vals, [num_outs])
  ref_vals_iter = iter(ref_vals)
  new_invals = tuple(next(ref_vals_iter) if isinstance(aval, AbstractRef)
                     else None for aval in in_avals)
  sentinel = object()
  assert next(ref_vals_iter, sentinel) is sentinel
  return new_invals, out_vals

