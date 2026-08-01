
def _base_newton_schulz_iteration(x: jax.Array, coeffs: jax.Array) -> jax.Array:
  # Implements Newton-Schulz step f(X) = c_0 X + c_1 (XX^T)X + c_2 (XX^T)^2X,
  # with quintic form f(X) = c_0 X + (c_1 A + c_2 AA)X, where A = XX^T.
  # The NS step has the property f(X) = f(X^T)^T. That is, we can get equivalent
  # result by transposing input and output. In particular, we may transpose X
  # when rows > cols for efficiency.
  a = x @ x.T.conj()
  b = coeffs[1] * a + coeffs[2] * a @ a
  return coeffs[0] * x + b @ x

