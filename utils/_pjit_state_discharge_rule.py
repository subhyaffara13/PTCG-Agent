
def _pjit_state_discharge_rule(
    in_avals, out_avals, *args, jaxpr, in_shardings, out_shardings,
    in_layouts, out_layouts, **params):
  if not (any(isinstance(e, RefEffect) for e in jaxpr.effects)
          or any(isinstance(a, AbstractRef) for a in jaxpr.in_avals)):
    # Only internal ref effects
    jaxpr_ = discharge_state(jaxpr)
    out = pjit.jit_p.bind(
        *args,
        jaxpr=jaxpr_,
        in_shardings=in_shardings,
        out_shardings=out_shardings,
        in_layouts=in_layouts,
        out_layouts=out_layouts,
        **params,
    )
    new_invals = [None] * len(in_avals)
    return new_invals, out
  if not all(isinstance(s, sharding_impls.UnspecifiedValue) for s in (*in_shardings, *out_shardings)):
    raise NotImplementedError

  if not (all(l is None for l in in_layouts) and
          all(l is None for l in out_layouts)):
    raise NotImplementedError

  discharged_jaxpr = discharge_state(jaxpr)
  new_in_shardings = (sharding_impls.UNSPECIFIED,) * len(discharged_jaxpr.in_avals)
  new_out_shardings = (sharding_impls.UNSPECIFIED,) * len(discharged_jaxpr.out_avals)
  new_in_layouts = (None,) * len(discharged_jaxpr.in_avals)
  new_out_layouts = (None,) * len(discharged_jaxpr.out_avals)
  out_and_ref_vals = pjit.jit_p.bind(
      *args, jaxpr=discharged_jaxpr, in_shardings=new_in_shardings,
      out_shardings=new_out_shardings, in_layouts=new_in_layouts,
      out_layouts=new_out_layouts, **params)
  out_vals, ref_vals = split_list(out_and_ref_vals, [len(jaxpr.out_avals)])
  ref_vals_iter = iter(ref_vals)
  new_invals = tuple(next(ref_vals_iter) if isinstance(aval, AbstractRef)
                     else None for aval in in_avals)
  sentinel = object()
  assert next(ref_vals_iter, sentinel) is sentinel
  return new_invals, out_vals

