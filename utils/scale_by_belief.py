
def scale_by_belief(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-16,
    eps_root: jax.typing.ArrayLike = 1e-16,
    *,
    nesterov: bool = False,
) -> base.GradientTransformation:
  """Rescale updates according to the AdaBelief algorithm.

  See :func:`optax.adabelief` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of variance of grads.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the second moment of the prediction error to improve
      numerical stability. If backpropagating gradients through the gradient
      transformation (e.g. for meta-learning), this must be non-zero.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    mu = optax.tree.zeros_like(params)  # First moment
    s = optax.tree.zeros_like(params)  # Second Central moment
    return ScaleByBeliefState(count=jnp.zeros([], jnp.int32), mu=mu, nu=s)

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    prediction_error = optax.tree.sub(updates, mu)
    nu = optax.tree.update_moment_per_elem_norm(prediction_error, state.nu, b2,
                                                2)
    nu = jax.tree.map(lambda v: v + eps_root, nu)
    count_inc = numerics.safe_increment(state.count)
    if nesterov:
      mu_hat = jax.tree.map(
          lambda m, g: b1 * m + (1 - b1) * g,
          optax.tree.bias_correction(
              mu, b1, numerics.safe_increment(count_inc)),
          optax.tree.bias_correction(updates, b1, count_inc))
    else:
      mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    nu_hat = optax.tree.bias_correction(nu, b2, count_inc)
    updates = jax.tree.map(
        lambda m, v: None if m is None else m / (jnp.sqrt(v) + eps),
        mu_hat,
        nu_hat,
        is_leaf=lambda x: x is None,
    )
    return updates, ScaleByBeliefState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

