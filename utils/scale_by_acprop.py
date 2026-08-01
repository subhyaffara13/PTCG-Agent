
def scale_by_acprop(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-16,
    eps_root: jax.typing.ArrayLike = 1e-16,
) -> base.GradientTransformation:
  """Rescale updates according to ACProp (asynchronous version of AdaBelief).

  See :func:`optax.contrib.acprop` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of variance of grads.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the second moment of the prediction error to improve
      numerical stability. If backpropagating gradients through the gradient
      transformation (e.g. for meta-learning), this must be non-zero.

  Returns:
    A `GradientTransformation` object.
  """

  def init_fn(params):
    mu = optax.tree.zeros_like(params)  # First moment
    s = optax.tree.zeros_like(params)  # Second Central moment
    return transform.ScaleByBeliefState(
        count=jnp.zeros([], jnp.int32), mu=mu, nu=s
    )

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    prediction_error = jax.tree.map(lambda g, m: g - m, updates, state.mu)
    nu = optax.tree.update_moment_per_elem_norm(prediction_error, state.nu, b2,
                                                2)
    nu = jax.tree.map(lambda v: v + eps_root, nu)
    count_inc = numerics.safe_increment(state.count)

    # On initial step, avoid division by zero and force nu_hat to be 1.
    initial = state.count == 0
    t = jnp.where(initial, count_inc, state.count)
    nu_hat = optax.tree.bias_correction(state.nu, b2, t)
    nu_hat = jax.tree.map(lambda x: jnp.where(initial, 1, x), nu_hat)

    updates = jax.tree.map(
        lambda m, v: m / (jnp.sqrt(v) + eps), updates, nu_hat
    )
    return updates, transform.ScaleByBeliefState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

