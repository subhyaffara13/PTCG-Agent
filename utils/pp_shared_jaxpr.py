
def pp_shared_jaxpr(
    name: str,
    jaxpr: Jaxpr,
    context: JaxprPpContext,
    settings: JaxprPpSettings,
) -> pp.Doc:
  eqns_fn = lambda: pp_eqns(jaxpr.eqns, context, settings)
  pp_skeleton = pp_jaxpr_skeleton(jaxpr, eqns_fn, context, settings)
  return pp.concat([
      pp.text("let "),
      pp.text(name, anchor=f"g_{name}"),
      pp.text(" = "),
      pp_skeleton,
      pp.text(" in"),
      pp.brk(),
  ])

