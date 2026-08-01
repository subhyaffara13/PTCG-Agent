
def pp_jaxpr_skeleton(jaxpr: Jaxpr, eqns_fn, context: JaxprPpContext,
                      settings: JaxprPpSettings) -> pp.Doc:
  constvars = pp_vars(jaxpr.constvars, context,
                      print_shapes=settings.print_shapes, is_binder=True)
  invars = pp_vars(jaxpr.invars, context, print_shapes=settings.print_shapes,
                   is_binder=True)
  eqns = eqns_fn()
  outvars = pp.concat([
    pp.text("("), pp_vars(jaxpr.outvars, context, separator=","),
    pp.text(")" if len(jaxpr.outvars) != 1 else ",)")])
  if settings.print_effects:
    # TODO(sharadmv): render an entire signature here
    eff_text = [pp.text(" : { ")]
    for i, eff in enumerate(jaxpr.effects):
      if i > 0:
        eff_text.append(pp.text(", "))
      eff_text.append(pp_effect(eff, context))
    eff_text.append(pp.text(" }"))
  else:
    eff_text = []
  return pp.group(pp.nest(2, pp.concat([
    pp.text("{ "), pp.keyword(pp.text("lambda ")),
    constvars, pp.text("; "), invars,
    pp.text(". "), pp.keyword(pp.text("let")),
    pp.nest(2, pp.brk() + eqns), pp.brk(),
    pp.keyword(pp.text("in ")), outvars,
    pp.concat(eff_text)
  ])) + pp.text(" }"))

