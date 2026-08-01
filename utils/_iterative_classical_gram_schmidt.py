
def _iterative_classical_gram_schmidt(Q, x, xnorm, max_iterations=2):
  """
  Orthogonalize x against the columns of Q. The process is repeated
  up to `max_iterations` times, or fewer if the condition
  ||r|| < (1/sqrt(2)) ||x|| is met earlier (see below for the meaning
  of r and x).

  Parameters
  ----------
  Q : array or tree of arrays
      A matrix of orthonormal columns.
  x : array or tree of arrays
      A vector. It will be replaced with a new vector q which is orthonormal
      to the columns of Q, such that x in span(col(Q), q).
  xnorm : float
      Norm of x.

  Returns
  -------
  q : array or tree of arrays
      A unit vector, orthonormal to each column of Q, such that
      x in span(col(Q), q).
  r : array
      Stores the overlaps of x with each vector in Q.
  """
  # "twice is enough"
  # http://slepc.upv.es/documentation/reports/str1.pdf

  # TODO(shoyer): consider switching to only one iteration, like SciPy?

  # This assumes that Q's leaves all have the same dimension in the last
  # axis.
  Q0 = tree_leaves(Q)[0]
  r = jnp.zeros(Q0.shape[-1], dtype=Q0.dtype)
  q = x
  xnorm_scaled = xnorm / jnp.sqrt(2.0)

  def body_function(carry):
    k, q, r, qnorm_scaled = carry
    h = _project_on_columns(Q, q)
    Qh = tree_map(lambda X: _dot(X, h), Q)
    q = _sub(q, Qh)
    r = _add(r, h)

    def qnorm_cond(carry):
      k, not_done, _, _ = carry
      return jnp.logical_and(not_done, k < (max_iterations - 1))

    def qnorm(carry):
      k, _, q, qnorm_scaled = carry
      _, qnorm = _safe_normalize(q)
      qnorm_scaled = qnorm / jnp.sqrt(2.0)
      return (k, False, q, qnorm_scaled)

    init = (k, True, q, qnorm_scaled)
    _, _, q, qnorm_scaled = lax.while_loop(qnorm_cond, qnorm, init)
    return (k + 1, q, r, qnorm_scaled)

  def cond_function(carry):
    k, _, r, qnorm_scaled = carry
    _, rnorm = _safe_normalize(r)
    return jnp.logical_and(k < (max_iterations - 1), rnorm < qnorm_scaled)

  k, q, r, qnorm_scaled = body_function((0, q, r, xnorm_scaled))
  k, q, r, _ = lax.while_loop(cond_function, body_function,
                              (k, q, r, qnorm_scaled))
  return q, r

