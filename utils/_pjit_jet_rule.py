
def _pjit_jet_rule(primals_in, series_in, **params):
  primals_and_series, in_tree_def = tree_flatten((primals_in, series_in))
  order = len(series_in[0])
  primals_and_series_avals = tuple(core.shaped_abstractify(x) for x in primals_and_series)
  jaxpr_jet, out_tree_def = _jet_jaxpr(params['jaxpr'], order,
                                       primals_and_series_avals, in_tree_def)
  num_series_in = len(primals_in) * order
  num_series_out = len(params['out_shardings']) * order
  new_params = {
      **params,
      'jaxpr': jaxpr_jet,
      'in_shardings': (
          params['in_shardings'] + (sharding_impls.UNSPECIFIED,) * num_series_in
      ),
      'out_shardings': (
          params['out_shardings']
          + (sharding_impls.UNSPECIFIED,) * num_series_out
      ),
      'in_layouts': params['in_layouts'] + (None,) * num_series_in,
      'out_layouts': params['out_layouts'] + (None,) * num_series_out,
      'donated_invars': params['donated_invars'] + (False,) * num_series_in,
  }
  result = pjit.jit_p.bind(*primals_and_series, **new_params)
  return tree_unflatten(out_tree_def(), result)

