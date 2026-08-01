
def _convert_elt_type_fwd_rule(eqn):
  t, = eqn.invars
  aval = t.aval
  if (aval.dtype == eqn.params['new_dtype'] and
      aval.weak_type == eqn.params['weak_type'] and
      not dtypes.issubdtype(aval.dtype, dtypes.extended) and
      (eqn.params['sharding'] is None or eqn.params['sharding'] == aval.sharding)):
    return [0], None
  else:
    return [None], eqn

