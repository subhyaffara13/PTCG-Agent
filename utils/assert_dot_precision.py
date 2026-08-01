
def assert_dot_precision(expected_precision, fun, *args):
  jaxpr = api.make_jaxpr(fun)(*args)
  precisions = [eqn.params['precision'] for eqn in iter_eqns(jaxpr.jaxpr)
                if eqn.primitive == lax.dot_general_p]
  for precision in precisions:
    msg = f"Unexpected precision: {expected_precision} != {precision}"
    if isinstance(precision, tuple):
      assert precision[0] == expected_precision, msg
      assert precision[1] == expected_precision, msg
    else:
      assert precision == expected_precision, msg

