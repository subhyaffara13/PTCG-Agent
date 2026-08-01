
def assert_dot_preferred_element_type(expected, fun, *args, **kwargs):
  jaxpr = api.make_jaxpr(partial(fun, **kwargs))(*args)
  pref_eltypes = [eqn.params['preferred_element_type'] for eqn in iter_eqns(jaxpr.jaxpr)
                   if eqn.primitive == lax.dot_general_p]
  for pref_eltype in pref_eltypes:
    msg = f"Unexpected preferred_element_type: {expected} != {pref_eltype}"
    assert expected == pref_eltype, msg

