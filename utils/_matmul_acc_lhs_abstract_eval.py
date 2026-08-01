
def _matmul_acc_lhs_abstract_eval(lhs: jax.Array, **_):
  del lhs  # Unused.
  return [], {mxu_effect}

