
def _broadcast_in_dim_pp_rule(eqn, context, settings):
  params = dict(eqn.params)
  if not params['broadcast_dimensions']:
    del params['broadcast_dimensions']  # don't show trivial case
  del params['shape']  # implied by let binder type
  params.pop('sharding', None)  # implied by let binder type
  return core._pp_eqn(eqn.replace(params=params), context, settings)

