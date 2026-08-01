
def schedule_free_adamw(
    learning_rate: jax.typing.ArrayLike = 0.0025,
    warmup_steps: Optional[int] = None,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
    weight_decay: jax.typing.ArrayLike = 0.0,
    weight_lr_power: jax.typing.ArrayLike = 2.0,
    state_dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.GradientTransformationExtraArgs:
  """Schedule-Free wrapper for AdamW.

  Shortcut example for using schedule_free with AdamW, which is a common use
  case. Note that this is just an example, and other usecases are possible, e.g.
  using a weight decay mask, nesterov, etc. Note also that the EMA parameter of
  the schedule free method (b1) must be strictly positive.

  Args:
    learning_rate: AdamW learning rate.
    warmup_steps: positive integer, the length of the linear warmup.
    b1: beta_1 parameter in the y update.
    b2: Exponential decay rate to track the second moment of past gradients.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    weight_decay: Strength of the weight decay regularization.
    weight_lr_power: we downweight the weight of averaging using this. This is
      especially helpful in early iterations during warmup.
    state_dtype: dtype for z sequence in the schedule free method.

  Returns:
    A :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.contrib.schedule_free_adamw(1.0)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  eval_params = optax.contrib.schedule_free_eval_params(
    ...      opt_state, params)
    ...  print('Objective function: {:.2E}'.format(f(eval_params)))
    Objective function: 5.00E+00
    Objective function: 3.05E+00
    Objective function: 1.73E+00
    Objective function: 8.94E-01
    Objective function: 4.13E-01

  .. note::
    Note that :func:`optax.scale_by_adam` with ``b1=0`` stores in its state an
    unused first moment always equal to zero. To avoid this waste of memory,
    we replace
    :func:`optax.scale_by_adam` with ``b1=0`` by the equivalent
    :func:`optax.scale_by_rms` with ``eps_in_sqrt=False, bias_correction=True``.

  """
  if warmup_steps is not None:
    learning_rate = _schedule.warmup_constant_schedule(
        init_value=0,
        peak_value=learning_rate,
        warmup_steps=warmup_steps,
    )
  # The following is the same as adamw, but with the momentum term removed.
  optimizer = combine.chain(
      transform.scale_by_rms(
          decay=b2, eps=eps, eps_in_sqrt=False, bias_correction=True
      ),
      _adding.add_decayed_weights(weight_decay),
      transform.scale_by_learning_rate(learning_rate),
  )
  return schedule_free(
      optimizer,
      learning_rate=learning_rate,
      b1=b1,
      weight_lr_power=weight_lr_power,
      state_dtype=state_dtype,
  )

