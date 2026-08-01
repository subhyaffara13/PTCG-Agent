
def pp_jaxprs(jaxprs: Sequence[ClosedJaxpr | Jaxpr],
              context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  jaxprs = [j.jaxpr if isinstance(j, ClosedJaxpr) else j for j in jaxprs]
  return pp.group(pp.concat([pp.nest(2, pp.concat([
      pp.text('('), pp.brk(""),
      pp.join(pp.brk(), map(lambda x: pp_jaxpr(x, context, settings), jaxprs))]
    )), pp.brk(""), pp.text(')')])
  )

