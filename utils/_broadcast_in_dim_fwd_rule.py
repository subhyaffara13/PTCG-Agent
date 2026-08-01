
def _broadcast_in_dim_fwd_rule(eqn):
  v, = eqn.invars
  if (core.definitely_equal_shape(eqn.params['shape'], v.aval.shape)
      and (eqn.params['sharding'] is None or
           eqn.params['sharding'] == v.aval.sharding)):
    return [0], None
  else:
    return [None], eqn

