
def pp_jaxpr_eqn_range(jaxpr: Jaxpr, lo: int, hi: int, context: JaxprPpContext,
                       settings: JaxprPpSettings) -> pp.Doc:
  lo = max(lo, 0)
  hi = max(lo, min(hi, len(jaxpr.eqns)))
  eqns = jaxpr.eqns[lo:hi]
  def eqns_fn():
    pps = []
    if len(eqns) == 0 and len(jaxpr.eqns) != 0:
      pps.append(pp.text('...'))
    else:
      if lo != 0:
        pps.append(pp.text('...'))
      pps.extend(map((lambda e: pp_eqn(e, context, settings)), eqns))
      if hi != len(jaxpr.eqns):
        pps.append(pp.text('...'))
    return pp.join(pp.brk("; "), pps)
  return pp_jaxpr_skeleton(jaxpr, eqns_fn, context, settings)

