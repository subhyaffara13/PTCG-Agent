
def log_cosh(
    predictions: jax.typing.ArrayLike,
    targets: Optional[jax.typing.ArrayLike] = None,
) -> jax.Array:
  """Calculates the log-cosh loss for a set of predictions.

  log(cosh(x)) is approximately `(x**2) / 2` for small x and `abs(x) - log(2)`
  for large x.  It is a twice differentiable alternative to the Huber loss.

  Args:
    predictions: a vector of arbitrary shape `[...]`.
    targets: a vector with shape broadcastable to that of `predictions`; if not
      provided then it is assumed to be a vector of zeros.

  Returns:
    the log-cosh loss, with same shape as `predictions`.

  References:
    Chen et al, `Log Hyperbolic Cosine Loss Improves Variational Auto-Encoder
    <https://openreview.net/pdf?id=rkglvsC9Ym>`, 2019
  """
  utils.check_subdtype(predictions, jnp.floating)
  errors = (predictions - targets) if (targets is not None) else predictions
  # log(cosh(x)) = log((exp(x) + exp(-x))/2) = log(exp(x) + exp(-x)) - log(2)
  return jnp.logaddexp(errors, -errors) - jnp.log(2.0).astype(errors.dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501

