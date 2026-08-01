
def pp_vars(vs: Sequence[Atom], context: JaxprPpContext,
            *, separator="", print_shapes: bool = False,
            is_binder: bool = False) -> pp.Doc:
  if print_shapes:
    return pp.nest(2, pp.group(
      pp.join(pp.text(separator) + pp.group(pp.brk()), [
        pp_var(v, context, is_binder=is_binder) +
        pp.type_annotation(pp.text(":" + pp_aval(v.aval, context)))
        for v in vs
      ])
    ))
  else:
    return pp.nest(2, pp.group(
      pp.join(pp.text(separator) + pp.group(pp.brk()),
              [pp_var(v, context, is_binder=is_binder) for v in vs])
    ))

