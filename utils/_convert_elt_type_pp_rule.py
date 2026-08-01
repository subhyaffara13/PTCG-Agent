
def _convert_elt_type_pp_rule(eqn, context, settings):
  params = dict(eqn.params)
  params.pop('sharding', None)  # implied by let binder type
  return core._pp_eqn(eqn.replace(params=params), context, settings)

