
def pp_jaxpr(
    jaxpr: Jaxpr,
    context: JaxprPpContext,
    settings: JaxprPpSettings,
) -> pp.Doc:
  if name := context.shared_jaxprs.get(jaxpr):
    return pp.text(name, href=f"#g_{name}")
  eqns_fn = lambda: pp_eqns(jaxpr.eqns, context, settings)
  return pp_jaxpr_skeleton(jaxpr, eqns_fn, context, settings)

