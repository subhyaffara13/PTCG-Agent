
def _pp_eqn(eqn: JaxprEqn, context: JaxprPpContext, settings: JaxprPpSettings,
            params: Sequence[str] | None = None) -> pp.Doc:
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  if params is None:
    params = sorted(eqn.params)
  name_stack_annotation = f'[{eqn.source_info.name_stack}]' if settings.name_stack else None
  lhs = pp_vars(eqn.outvars, context, print_shapes=settings.print_shapes,
                is_binder=True)
  rhs = [pp.text(eqn.primitive.name, annotation=name_stack_annotation),
         pp_kv_pairs([(p, eqn.params[p]) for p in params], context, settings),
         pp.text(" ") + pp_vars(eqn.invars, context)]
  if eqn.outvars:
    return pp.concat([lhs, pp.text(" = ", annotation=annotation), *rhs])
  else:
    return pp.concat(rhs)

