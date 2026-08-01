
def schedule_free(
    base_optimizer: base.GradientTransformation,
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    weight_lr_power: jax.typing.ArrayLike = 2.0,
    state_dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.GradientTransformationExtraArgs:
  r"""Turn base_optimizer schedule_free.

  Accumulates updates returned by the base_optimizer w/o Momentum and
  replaces the momentum of an underlying optimizer with a combination of
  interpolation and averaging. In the case of gradient descent the update is

  .. math::

    \begin{align*}
      y_{t} & = (1-\beta_1)z_{t} + \beta_1 x_{t},\\
      z_{t+1} & =z_{t}-\gamma\nabla f(y_{t}),\\
      x_{t+1} & =\left(1-\frac{1}{t}\right)x_{t}+\frac{1}{t}z_{t+1},
    \end{align*}

  Here :math:`x` is the sequence that evaluations of test/val loss should occur
  at,  which differs from the primary iterates :math:`z` and the gradient
  evaluation locations :math:`y`. The updates to :math:`z` correspond to the
  underlying optimizer, in this case a simple gradient step. Note that,
  :math:`\beta_1` corresponds to `b1` in the code.

  As the name suggests, Schedule-Free learning does not require a decreasing
  learning rate schedule, yet typically out-performs, or at worst matches, SOTA
  schedules such as cosine-decay and linear decay. Only two sequences need to be
  stored at a time (the third can be computed from the other two on the fly) so
  this method has the same memory requirements as the base optimizer (parameter
  buffer + momentum).

  In practice, authors recommend tuning :math:`\beta_1`, `warmup_steps` and
  `peak_lr` for each problem separately. Default for :math:`\beta_1` is 0.9 but
  `0.95` and `0.98` may also work well. Schedule-Free can be wrapped on top of
  any optax optimizer. At test time, the parameters should be evaluated using
  :func:`optax.contrib.schedule_free_eval_params` as presented below.

  For example, change this::

    learning_rate_fn = optax.warmup_cosine_decay_schedule(peak_value=tuned_lr)
    optimizer = optax.adam(learning_rate_fn, b1=b1)

  To::

    learning_rate_fn = optax.warmup_constant_schedule(peak_value=retuned_lr)
    optimizer = optax.adam(learning_rate_fn, b1=0.)
    optimizer = optax.contrib.schedule_free(optimizer, learning_rate_fn, b1=b1)
    ..
    params_for_eval = optax.contrib.schedule_free_eval_params(state, params)

  Especially note that is important to switch off Momentum of the base
  optimizer. As of Apr, 2024, schedule_free is tested with SGD and Adam.

  Args:
    base_optimizer: Base optimizer to compute updates from.
    learning_rate: learning_rate schedule w/o decay but with warmup.
    b1: beta_1 parameter in the y update.
    weight_lr_power: we downweight the weight of averaging using this. This is
      especially helpful in early iterations during warmup.
    state_dtype: dtype for z sequence in the schedule free method.

  Returns:
    A :class:`optax.GradientTransformationExtraArgs`.

  References:
    Defazio et al, `The Road Less Scheduled
    <https://arxiv.org/abs/2405.15682>`_, 2024

    Defazio et al, `Schedule-Free Learning - A New Way to Train
    <https://github.com/facebookresearch/schedule_free/tree/main>`_, 2024

  .. warning::
    The current implementation requires the parameter ``b1`` to be strictly
    positive.
  """
  base_optimizer = base.with_extra_args_support(base_optimizer)

  def init_fn(params: base.Params) -> ScheduleFreeState:
    # Define state parameters with the lowest dtype of the parameters to avoid
    # dtype promotion of parameters resulting in a dtype mismatch between
    # parameters and updates.
    params_dtype = optax.tree.dtype(params, 'lowest')
    if state_dtype is not None:
      z = optax.tree.cast(params, dtype=state_dtype)
    else:
      z = params
    # It's important to copy the params here so that z is a distinct array and
    # we can donate both z and the params to JITted functions.
    z = jax.tree.map(lambda t: t.copy(), z)
    return ScheduleFreeState(
        b1=jnp.asarray(b1, dtype=params_dtype),
        weight_sum=jnp.zeros([], dtype=params_dtype),
        step_count=jnp.ones([], dtype=jnp.int32),
        max_lr=jnp.zeros([], dtype=params_dtype),
        base_optimizer_state=base_optimizer.init(params),
        z=z,
    )

  def update_fn(
      grads: base.Updates,
      state: ScheduleFreeState,
      params: Optional[base.Params] = None,
      **extra_args,
  ):
    lr = learning_rate
    if callable(learning_rate):
      lr = jnp.asarray(
          learning_rate(state.step_count), dtype=state.max_lr.dtype  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
      )
    max_lr = jnp.maximum(state.max_lr, lr)

    next_step_count = numerics.safe_increment(state.step_count)

    weight = max_lr**weight_lr_power
    next_total_weight = state.weight_sum + weight
    # We add this to avoid NaNs in the case of a small learning rate.
    ck = jnp.where(
        jnp.logical_or(jnp.isnan(weight), jnp.isnan(next_total_weight)),
        jnp.full(weight.shape, jnp.nan),
        jnp.nan_to_num(weight / next_total_weight, nan=0.0, posinf=jnp.inf),
    )

    base_updates, next_base_optimizer_state = base_optimizer.update(
        grads,
        state.base_optimizer_state,
        params,
        **extra_args,
    )
    z = jax.tree.map(
        lambda pi, ui: jnp.asarray(pi + ui).astype(jnp.asarray(pi).dtype),
        state.z,
        base_updates,
    )

    # Important: recompute x to both save memory and maintain accurate x seq
    # especially if y is modified by another transform wrapped on top.
    prev_x = jax.tree.map(
        lambda yi, zi: (yi - (1.0 - b1) * zi) / b1, params, state.z
    )

    x = jax.tree.map(
        lambda xi, zi: (1.0 - ck) * xi + ck * zi,
        prev_x,
        z,
    )
    new_params = jax.tree.map(
        lambda xi, zi: b1 * xi + (1.0 - b1) * zi,
        x,
        z,
    )
    updates = jax.tree.map(lambda npi, pi: npi - pi, new_params, params)

    next_state = ScheduleFreeState(
        b1=state.b1,
        weight_sum=next_total_weight,
        step_count=next_step_count,
        max_lr=max_lr,
        base_optimizer_state=next_base_optimizer_state,
        z=z,
    )

    return updates, next_state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

