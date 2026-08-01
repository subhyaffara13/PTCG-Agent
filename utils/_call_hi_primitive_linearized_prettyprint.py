
def _call_hi_primitive_linearized_prettyprint(eqn, context, settings):
  params = dict(eqn.params, _prim=str(eqn.params['_prim'].__class__),
                residuals_tree='...')
  return core._pp_eqn(eqn.replace(params=params), context, settings)

