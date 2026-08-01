
def _cond_wrapper(t_fn, f_fn, scope, pred, *ops, variables, rngs):
  return lift.cond(
    pred, t_fn, f_fn, scope, *ops, variables=variables, rngs=rngs
  )

