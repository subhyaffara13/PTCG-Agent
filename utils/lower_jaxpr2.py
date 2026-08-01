
def lower_jaxpr2(hi_jaxpr) -> ClosedJaxpr:
  in_avals = FlatTree.flatten(([a.lo_ty() for a in hi_jaxpr.in_aval_qdds], {}))
  lo_jaxpr, _ = lower_jaxpr(hi_jaxpr, in_avals)
  return lo_jaxpr

