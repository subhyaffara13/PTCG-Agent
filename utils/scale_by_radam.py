
def scale_by_radam(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    threshold: jax.typing.ArrayLike = 5.0,
    *,
    nesterov: bool = False,
) -> base.GradientTransformation:
  """Rescale updates according to the Rectified Adam algorithm.

  See :func:`optax.radam` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.
    threshold: Threshold for variance tractability.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  ro_inf = 2.0 / (1.0 - b2) - 1.0

  def _radam_update(ro, mu_hat, nu_hat):
    r = jnp.sqrt(
        (ro - 4.0)
        * (ro - 2.0)
        * ro_inf
        / ((ro_inf - 4.0) * (ro_inf - 2.0) * ro)
    )
    updates = jax.tree.map(
        lambda m, v: r.astype(m.dtype) * m / (jnp.sqrt(v + eps_root) + eps),
        mu_hat,
        nu_hat,
    )
    return updates

  def init_fn(params):
    mu = optax.tree.zeros_like(params)  # First moment
    nu = optax.tree.zeros_like(params)  # Second moment
    return ScaleByAdamState(count=jnp.zeros([], jnp.int32), mu=mu, nu=nu)

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, b2, 2)
    count_inc = numerics.safe_increment(state.count)
    b2t = b2**count_inc
    ro = ro_inf - 2 * count_inc * b2t / (1 - b2t)
    if nesterov:
      mu_hat = jax.tree.map(
          lambda m, g: b1 * m + (1 - b1) * g,
          optax.tree.bias_correction(mu, b1,
                                     numerics.safe_increment(count_inc)),
          optax.tree.bias_correction(updates, b1, count_inc),
      )
    else:
      mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    nu_hat = optax.tree.bias_correction(nu, b2, count_inc)
    updates = jax.tree.map(
        lambda t, f: jnp.where(ro >= threshold, t, f),
        _radam_update(ro, mu_hat, nu_hat),
        mu_hat,
    )
    return updates, ScaleByAdamState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

