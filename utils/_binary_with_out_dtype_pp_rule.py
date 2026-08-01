
def _binary_with_out_dtype_pp_rule(eqn, context, settings):
  params = dict(eqn.params)
  if params['out_dtype'] is None:
    del params['out_dtype']  # don't show trivial case
  return core._pp_eqn(eqn.replace(params=params), context, settings)

