
def _gaussian_kernel_eval(in_log, points, values, xi, precision):
  points, values, xi, precision = promote_dtypes_inexact(
      points, values, xi, precision)
  d = points.shape[1]

  if xi.shape[1] != d:
    raise ValueError("points and xi must have same trailing dim")
  if precision.shape != (d, d):
    raise ValueError("precision matrix must match data dims")

  whitening = linalg.cholesky(precision, lower=True)
  points = jnp.dot(points, whitening)
  xi = jnp.dot(xi, whitening)
  log_norm = jnp.sum(jnp.log(
      jnp.diag(whitening))) - 0.5 * d * jnp.log(2 * np.pi)

  def kernel(x_test, x_train, y_train):
    arg = log_norm - 0.5 * jnp.sum(jnp.square(x_train - x_test))
    if in_log:
      return jnp.log(y_train) + arg
    else:
      return y_train * jnp.exp(arg)

  reduce = special.logsumexp if in_log else jnp.sum
  reduced_kernel = lambda x: reduce(api.vmap(kernel, in_axes=(None, 0, 0))
                                    (x, points, values),
                                    axis=0)
  mapped_kernel = api.vmap(reduced_kernel)

  return mapped_kernel(xi)

