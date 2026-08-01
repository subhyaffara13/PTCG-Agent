
def pp_eqn(eqn: JaxprEqn, context: JaxprPpContext, settings: JaxprPpSettings
           ) -> pp.Doc:
  rule = (_pp_eqn if not settings.custom_pp_eqn_rules else
          pp_eqn_rules.get(eqn.primitive, _pp_eqn))
  doc = rule(eqn, context, settings)
  return (doc if eqn.source_info.traceback is None
          else pp.source_map(doc, eqn.source_info.traceback))

