import functools

def _lobpcg_standard_matrix(
    A: jax.Array,
    X: jax.Array,
    m: int,
    tol: jax.Array | float | None,
    debug: bool = False):
  """Computes lobpcg_standard(), possibly with debug diagnostics."""
  return _lobpcg_standard_callable(
      functools.partial(_mm, A), X, m, tol, debug)

