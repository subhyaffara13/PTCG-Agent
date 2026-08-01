
def _pjit_pp_rule(eqn: core.JaxprEqn,
                  context: core.JaxprPpContext,
                  settings: core.JaxprPpSettings) -> core.pp.Doc:
  params = dict(eqn.params)
  del params['inline']
  if not any(params['donated_invars']):
    del params['donated_invars']
  if all(isinstance(s, UnspecifiedValue) for s in params['in_shardings']):
    del params['in_shardings']
  if all(isinstance(s, UnspecifiedValue) for s in params['out_shardings']):
    del params['out_shardings']
  if all(l is None for l in params['in_layouts']):
    del params['in_layouts']
  if all(l is None for l in params['out_layouts']):
    del params['out_layouts']
  if not params['keep_unused']:
    del params['keep_unused']
  if params['ctx_mesh'].empty:
    del params['ctx_mesh']
  if not params['compiler_options_kvs']:
    del params['compiler_options_kvs']

  if params['jaxpr'].jaxpr not in context.shared_jaxprs:
    context.suggest_same_var_names(params['jaxpr'].jaxpr.invars, eqn.invars)
    context.suggest_same_var_names(params['jaxpr'].jaxpr.outvars, eqn.outvars)

  # Move name= to the front to make the resulting equation easier to scan.
  del params["name"]
  return core._pp_eqn(eqn, context, settings, params=["name"] + sorted(params))

