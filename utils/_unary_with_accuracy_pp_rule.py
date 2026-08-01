
def _unary_with_accuracy_pp_rule(eqn, context, settings):
  params = dict(eqn.params)
  if 'accuracy' in params and params['accuracy'] is None:
    del params['accuracy']
  return core._pp_eqn(eqn.replace(params=params), context, settings)

