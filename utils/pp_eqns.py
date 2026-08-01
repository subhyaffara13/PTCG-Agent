
def pp_eqns(eqns: Sequence[JaxprEqn],
            context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  return pp.join(
    pp.brk("; "),
    [pp_eqn(e, context, settings) for e in eqns])

