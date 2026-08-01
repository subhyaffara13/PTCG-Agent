
def _sinc_maclaurin(k, x):
  # compute the kth derivative of x -> sin(x)/x evaluated at zero (since we
  # compute the monomial term in the jvp rule)
  # TODO(mattjj): see https://github.com/jax-ml/jax/issues/10750
  if k % 2:
    return x * 0
  else:
    return x * 0 + _lax_const(x, (-1) ** (k // 2) / (k + 1))

