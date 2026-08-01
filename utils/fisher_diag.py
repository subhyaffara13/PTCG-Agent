
def fisher_diag(
    negative_log_likelihood: LossFn,
    params: Any,
    inputs: jax.Array,
    targets: jax.Array,
) -> jax.Array:
  """Computes the diagonal of the (observed) Fisher information matrix.

  .. deprecated: 0.2.7. This function will be removed in 0.2.9

  Args:
    negative_log_likelihood: the negative log likelihood function with expected
      signature `loss = fn(params, inputs, targets)`.
    params: model parameters.
    inputs: inputs at which `negative_log_likelihood` is evaluated.
    targets: targets at which `negative_log_likelihood` is evaluated.

  Returns:
    An Array corresponding to the product to the Hessian of
    `negative_log_likelihood` evaluated at `(params, inputs, targets)`.
  """
  return jnp.square(
      _ravel(jax.grad(negative_log_likelihood)(params, inputs, targets))
  )

