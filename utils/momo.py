
def momo(
    learning_rate: base.ScalarOrSchedule = 1.0,
    beta: jax.typing.ArrayLike = 0.9,
    lower_bound: jax.typing.ArrayLike = 0.0,
    weight_decay: jax.typing.ArrayLike = 0.0,
    adapt_lower_bound: bool = False,
) -> base.GradientTransformationExtraArgs:
  """Adaptive Learning Rates for SGD with momentum.

  MoMo typically needs less tuning for value of ``learning_rate``,
  by exploiting the fact that a lower bound of the loss (or the optimal value)
  is known. For most tasks, zero is a lower bound and an accurate estimate of
  the final loss.

  MoMo performs SGD with momentum with a Polyak-type learning rate. The
  effective step size is ``min(learning_rate, <adaptive term>)``, where the
  adaptive term is computed on the fly.

  Note that one needs to pass the latest (batch) loss value to the update
  function using the keyword argument ``value``.

  Args:
    learning_rate: User-specified learning rate. Recommended to be chosen rather
      large, by default 1.0.
    beta: Momentum coefficient (for EMA).
    lower_bound: Lower bound of the loss. Zero should be a good choice for many
      tasks.
    weight_decay: Weight-decay parameter.
    adapt_lower_bound: If no good guess for the lower bound is available, set
      this to true, in order to estimate the lower bound on the fly (see the
      paper for details).

  Returns:
    A :class:`optax.GradientTransformation` object.

  Examples:
    >>> from optax import contrib
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = contrib.momo()
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  value, grad = jax.value_and_grad(f)(params)
    ...  params, opt_state = solver.update(grad, opt_state, params, value=value)
    ...  print('Objective function: ', f(params))
    Objective function:  3.5
    Objective function:  0.0
    Objective function:  0.0
    Objective function:  0.0
    Objective function:  0.0

  References:
    Schaipp et al., `MoMo: Momentum Models for Adaptive Learning Rates
    <https://arxiv.org/abs/2305.07583>`_, 2023

  .. versionadded:: 0.2.3
  """

  def init_fn(params: base.Params) -> MomoState:
    # Define state parameters with the lowest dtype of the parameters to avoid
    # dtype promotion of parameters resulting in a dtype mismatch between
    # parameters and updates.
    params_dtype = optax.tree.dtype(params, 'lowest')
    exp_avg = optax.tree.zeros_like(params)
    barf = jnp.zeros([], dtype=params_dtype)
    gamma = jnp.zeros([], dtype=params_dtype)
    init_lb = jnp.array(lower_bound, dtype=params_dtype)
    count = jnp.zeros([], jnp.int32)
    return MomoState(exp_avg, barf, gamma, init_lb, count)

  def update_fn(
      updates: base.Updates,
      state: MomoState,
      params: Optional[base.Params],
      *,
      value: jax.typing.ArrayLike,
      **extra_args,
  ) -> tuple[base.Updates, MomoState]:
    # complies with signature of GradientTransformationExtraArgs but ignores the
    # extra_args
    del extra_args
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)
    if value is None:
      raise ValueError("""You need to pass the latest loss value to Momo.
                       Use ``jax.value_and_grad`` for this.""")
    count = state.count
    # initialize at first gradient, and loss
    bt = jnp.where(count == 0, 0.0, beta)
    barf = bt * state.barf + (1 - bt) * jnp.asarray(
        value, dtype=state.barf.dtype  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    )
    exp_avg = jax.tree.map(
        lambda ea, g: bt * ea + (1 - bt) * g, state.exp_avg, updates
    )
    gamma = bt * state.gamma + (1 - bt) * optax.tree.vdot(updates, params)
    exp_avg_norm = optax.tree.norm(exp_avg, squared=True)
    iprod = optax.tree.vdot(exp_avg, params)
    alpha = learning_rate(count) if callable(learning_rate) else learning_rate
    # Reset lower bound
    if adapt_lower_bound:
      cap = (1 + alpha * weight_decay) * (barf - gamma) + iprod
      this_lb = lax.cond(
          cap < (1 + alpha * weight_decay) * state.lb,
          lambda: jnp.maximum(
              cap / (2 * (1 + alpha * weight_decay)), lower_bound
          ),
          lambda: state.lb,
      )
    else:
      this_lb = state.lb
    t1 = jnp.maximum(
        (1 + alpha * weight_decay) * (barf - this_lb - gamma) + iprod, 0.0
    ) / (exp_avg_norm)
    # if denom is zero, take no step
    t1 = jnp.where(exp_avg_norm <= jnp.finfo(float).eps, 0.0, t1)
    tau = jnp.minimum(alpha, t1)
    p_update = jax.tree.map(
        lambda ea, p: -(alpha * weight_decay) / (1 + alpha * weight_decay) * p
        - tau * ea,
        exp_avg,
        params,
    )
    if adapt_lower_bound:
      new_lb = jnp.maximum(
          (barf + iprod - gamma) - (1 / 2) * tau * exp_avg_norm, lower_bound
      )
    else:
      new_lb = state.lb
    new_state = MomoState(
        exp_avg=exp_avg,
        barf=barf,
        gamma=gamma,
        lb=new_lb,
        count=numerics.safe_increment(count),
    )
    return p_update, new_state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

