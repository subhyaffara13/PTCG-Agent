
def _pallas_call_typecheck_rule(ctx_factory, *in_atoms, grid_mapping, **params):
  in_avals = [x.aval for x in in_atoms]
  with grid_mapping.trace_env():
    return pallas_call_p.abstract_eval(
        *in_avals, grid_mapping=grid_mapping, **params
    )

