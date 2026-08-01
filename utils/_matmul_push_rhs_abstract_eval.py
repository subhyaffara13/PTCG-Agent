
def _matmul_push_rhs_abstract_eval(ref: jax.Array, **_):
  del ref  # Unused.
  return [], {mxu_effect}

