from typing import Optional

def schedule_free_sgd(
    learning_rate: jax.typing.ArrayLike = 1.0,
    warmup_steps: Optional[int] = None,
    b1: jax.typing.ArrayLike = 0.9,
    weight_decay: Optional[jax.typing.ArrayLike] = None,
    weight_lr_power: jax.typing.ArrayLike = 2.0,
    state_dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.GradientTransformationExtraArgs:
  """Schedule-Free wrapper for SGD.

  Shortcut example for using schedule_free with SGD, which is a common use case.
  Note that this is just an example, and other use cases are possible, e.g.
  using a weight decay mask. Note also that the EMA parameter of the
  schedule free method (b1) must be strictly positive.

  Args:
    learning_rate: SGD learning rate.
    warmup_steps: positive integer, the length of the linear warmup.
    b1: beta_1 parameter in the y update.
    weight_decay: Strength of the weight decay regularization. Note that this
      weight decay is multiplied with the learning rate. This is consistent with
      other frameworks such as PyTorch, but different from (Loshchilov et al,
      2019) where the weight decay is only multiplied with the "schedule
      multiplier", but not the base learning rate.
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
    >>> solver = optax.contrib.schedule_free_sgd()
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
    Objective function: 1.40E+01
    Objective function: 1.75E-14
    Objective function: 9.96E-01
    Objective function: 8.06E-01
    Objective function: 2.41E-01
  """
  if warmup_steps is not None:
    learning_rate = _schedule.warmup_constant_schedule(
        init_value=0,
        peak_value=learning_rate,
        warmup_steps=warmup_steps,
    )
  optimizer = alias.sgd(learning_rate)
  if weight_decay is not None:
    optimizer = combine.chain(
        _adding.add_decayed_weights(weight_decay), optimizer
    )
  return schedule_free(
      optimizer,
      learning_rate=learning_rate,
      b1=b1,
      weight_lr_power=weight_lr_power,
      state_dtype=state_dtype,
  )

