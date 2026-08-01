
def scale_by_sophia(
    b1: jax.typing.ArrayLike = 0.965,
    b2: jax.typing.ArrayLike = 0.99,
    eps: jax.typing.ArrayLike = 1e-8,
    gamma: jax.typing.ArrayLike = 0.01,
    clip_threshold: Optional[jax.typing.ArrayLike] = 1.0,
    update_interval: jax.typing.ArrayLike = 10,
    hessian_diagonal_fn: Union[
        base.GradientTransformation,
        base.GradientTransformationExtraArgs,
    ] = hutchinson_estimator_diag_hessian(),
    mu_dtype: Optional[Any] = None,
    verbose: bool = False,
    print_win_rate_every_n_steps: jax.typing.ArrayLike = 0,
) -> base.GradientTransformationExtraArgs:
  """Sophia optimizer.

  See :func:`optax.contrib.sophia` for more details.

  Args:
    b1: Exponential decay rate for the first moment estimates.
    b2: Exponential decay rate for the hessian diagonal estimates. Keep in mind
      effective `b2` is `1 - (1 - b2) / update_interval`, e.g. default `b2` of
      0.99 is effectively 0.999 because default `update_interval` is every 10.
    eps: Small constant to avoid division by zero.
    gamma: Normalizing constant for the hessian diagonal.
    clip_threshold: Threshold for clipping updates.
    update_interval: Interval for updating the hessian diagonal.
    hessian_diagonal_fn: GradientTransformation that computes the diagonal of
      the Hessian. Default is Hutchinson's estimator (sophia-h). If using more
      than one device, be sure this function properly averages the hessian
      diagonal across devices.
    mu_dtype: dtype of the first moment estimates.
    verbose: If True, print win rate every n steps.
    print_win_rate_every_n_steps: Print sophia win rate every n steps for
      diagnostic purposes. Authors state this value should stay between 0.1 and
      0.5 during training. If win rate is too low, try increasing `gamma`. 0 to
      turn off.

  Returns:
    optax.GradientTransformationExtraArgs
  """
  mu_dtype = utils.canonicalize_dtype(mu_dtype)
  hessian_diagonal_fn = base.with_extra_args_support(hessian_diagonal_fn)

  def init_fn(params):
    return SophiaState(
        count=jnp.zeros([], jnp.int32),
        mu=optax.tree.zeros_like(params, dtype=mu_dtype),
        nu=optax.tree.zeros_like(params),
        hessian_fn_state=hessian_diagonal_fn.init(params),
    )

  def update_fn(updates, state: SophiaState, params=None, **hess_fn_kwargs):
    if params is None:
      raise ValueError("params must be provided to sophia's update function.")
    count_inc = numerics.safe_int32_increment(state.count)

    grads = updates

    # Sophia update
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    updates = jax.tree.map(
        lambda m, h: m / jnp.maximum(gamma * h, eps), mu_hat, state.nu
    )
    if clip_threshold is not None:
      sum_not_clipped = jax.tree.reduce(
          lambda x, y: x + y,
          jax.tree.map(lambda u: jnp.sum(jnp.abs(u) < clip_threshold), updates),
      )
      if verbose:
        win_rate = sum_not_clipped / optax.tree.size(updates)
        jax.lax.cond(
            count_inc % print_win_rate_every_n_steps == 0,
            lambda: jax.debug.print("Sophia optimizer win rate: {}", win_rate),
            lambda: None,
        )

      updates = jax.tree.map(
          lambda u: jnp.clip(u, -clip_threshold, clip_threshold), updates
      )

    # Hessian diagonal update
    def update_hessian_diag(hess_fn_state, nu):
      hessian_diag, hess_fn_state = hessian_diagonal_fn.update(
          grads, hess_fn_state, params=params, **hess_fn_kwargs
      )

      # ema of hessian diagonal
      nu = optax.tree.update_moment(hessian_diag, nu, b2, 1)

      return hess_fn_state, nu

    hessian_fn_state, nu = jax.lax.cond(
        jnp.equal(state.count % update_interval, 0),
        update_hessian_diag,
        lambda h, n: (h, n),
        state.hessian_fn_state,
        state.nu,
    )

    # Cast momentum back to mu_dtype
    mu = optax.tree.cast(mu, mu_dtype)

    state = SophiaState(
        count=count_inc,
        mu=mu,
        nu=nu,
        hessian_fn_state=hessian_fn_state,
    )
    return updates, state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

