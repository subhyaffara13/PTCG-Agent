
def _remat_state_discharge_rule(
    in_avals, out_avals, *args, jaxpr, **params):
  discharged_jaxpr = discharge.discharge_state(core.ClosedJaxpr(jaxpr, []))
  if discharged_jaxpr.consts:
    raise NotImplementedError
  out_vals_ref_vals = remat_p.bind(
      *args, jaxpr=discharged_jaxpr.jaxpr, **params
  )
  out_vals, ref_vals = split_list(out_vals_ref_vals, [len(jaxpr.outvars)])
  ref_vals_ = iter(ref_vals)
  new_invals = [next(ref_vals_) if isinstance(a, AbstractRef) else None
                for a in in_avals]
  assert next(ref_vals_, None) is None
  return new_invals, out_vals

