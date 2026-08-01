
def _integer_pow_sparse(spenv, *spvalues, y):
  if y <= 0:
    raise NotImplementedError(f"sparse rule for {lax.integer_pow_p} with non-positive exponent {y} is "
                              "not implemented because it would result in dense output. If this is your "
                              "intent, use sparse.todense() to convert your argument to a dense array.")
  return _zero_preserving_unary_op(lax.integer_pow_p, False)(spenv, *spvalues, y=y)

