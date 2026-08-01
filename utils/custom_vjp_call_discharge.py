
def custom_vjp_call_discharge(in_avals, out_avals, *args, call_jaxpr,
                              fwd_jaxpr_thunk, bwd, out_trees, symbolic_zeros,
                              num_consts):
  # Discharge happens after all AD is done, so we can discard the AD rules.
  del fwd_jaxpr_thunk, bwd, out_trees, symbolic_zeros, num_consts
  dis_closed_jaxpr = discharge_state(call_jaxpr)
  dis_jaxpr, dis_consts = dis_closed_jaxpr.jaxpr, dis_closed_jaxpr.consts
  outs = _eval_jaxpr_ad_error(dis_jaxpr, dis_consts, args)
  out_vals, ref_vals = split_list(outs, [len(call_jaxpr.out_avals)])
  ref_vals_ = iter(ref_vals)
  new_invals = [next(ref_vals_) if isinstance(aval, AbstractRef) else None
                for aval in in_avals]
  assert next(ref_vals_, None) is None
  return new_invals, out_vals

