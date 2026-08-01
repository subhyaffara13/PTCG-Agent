
def _pp_check(eqn, context, settings) -> core.pp.Doc:
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  name_stack_annotation = (f'[{eqn.source_info.name_stack}]'
                           if settings.name_stack else None)
  trimmed_params = sorted((k, v) for (k, v) in eqn.params.items()
                          if k != "err_tree")
  rhs = [core.pp.text(eqn.primitive.name, annotation=name_stack_annotation),
         core.pp_kv_pairs(trimmed_params, context, settings),
         core.pp.text(" ") + core.pp_vars(eqn.invars, context)]
  return core.pp.concat([core.pp.text("", annotation), *rhs])

