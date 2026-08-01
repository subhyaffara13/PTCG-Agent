
def scale_by_amsgrad(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
    bias_correction_mu: bool = True,
    bias_correction_nu: bool = True,
) -> base.GradientTransformation:
  """Rescale updates according to the AMSGrad algorithm.

  See :func:`optax.amsgrad` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    bias_correction_mu: Whether to apply bias correction to the first moment
      estimate. Set to ``False`` to match the original AMSGrad paper.
    bias_correction_nu: Whether to apply bias correction to the second moment
      estimate before taking the elementwise maximum (``nu_max``). Set to
      ``False`` to match the original AMSGrad paper.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params):
    mu = optax.tree.zeros_like(params, dtype=mu_dtype)  # First moment
    nu = optax.tree.zeros_like(params)  # Second moment
    nu_max = optax.tree.zeros_like(params)
    return ScaleByAmsgradState(
        count=jnp.zeros([], jnp.int32), mu=mu, nu=nu, nu_max=nu_max
    )

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, b2, 2)
    count_inc = numerics.safe_increment(state.count)

    if bias_correction_mu:
      mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    else:
      mu_hat = mu

    if bias_correction_nu:
      nu_eff = optax.tree.bias_correction(nu, b2, count_inc)
    else:
      nu_eff = nu

    nu_max = jax.tree.map(jnp.maximum, state.nu_max, nu_eff)
    updates = jax.tree.map(
        lambda m, v: None if m is None else m / (jnp.sqrt(v + eps_root) + eps),
        mu_hat,
        nu_max,
        is_leaf=lambda x: x is None,
    )
    mu = optax.tree.cast(mu, mu_dtype)
    return updates, ScaleByAmsgradState(
        count=count_inc, mu=mu, nu=nu, nu_max=nu_max
    )

  return base.GradientTransformation(init_fn, update_fn)

