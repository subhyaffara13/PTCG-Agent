
def lookahead(
    fast_optimizer: base.GradientTransformation,
    sync_period: jax.typing.ArrayLike,  # int
    slow_step_size: jax.typing.ArrayLike,  # float
    reset_state: bool = False,
) -> base.GradientTransformation:
  """Lookahead optimizer.

  Performs steps with a fast optimizer and periodically updates a set of slow
  parameters. Optionally resets the fast optimizer state after synchronization
  by calling the init function of the fast optimizer.

  Updates returned by the lookahead optimizer should not be modified before they
  are applied, otherwise fast and slow parameters are not synchronized
  correctly.

  Args:
    fast_optimizer: The optimizer to use in the inner loop of lookahead.
    sync_period: Number of fast optimizer steps to take before synchronizing
      parameters. Must be >= 1.
    slow_step_size: Step size of the slow parameter updates.
    reset_state: Whether to reset the optimizer state of the fast optimizer
      after each synchronization.

  Returns:
    A :class:`optax.GradientTransformation` with init and update functions. The
    updates passed to the update function should be calculated using the fast
    lookahead parameters only.

  Example:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> fast_opt = optax.sgd(1e-2)
    >>> opt = optax.lookahead(fast_opt, sync_period=5, slow_step_size=0.5)
    >>> params = optax.LookaheadParams.init_synced(jnp.ones((2,)))
    >>> state = opt.init(params)
    >>> loss_fn = lambda p: jnp.sum(p**2)
    >>> # Calculate gradients wrt the fast parameters
    >>> grads = jax.grad(loss_fn)(params.fast)
    >>> updates, state = opt.update(grads, state, params)
    >>> params = optax.apply_updates(params, updates)
    >>> # Calculate the eval loss wrt the slow parameters
    >>> loss_fn(params.slow)
    Array(2., dtype=float32)

  References:
    Zhang et al, `Lookahead Optimizer: k steps forward, 1 step back
    <https://arxiv.org/abs/1907.08610>`_, 2019
  """
  if sync_period < 1:
    raise ValueError('Synchronization period must be >= 1.')

  def init_fn(params: base.Params) -> LookaheadState:
    fast_params = getattr(params, 'fast', None)
    if fast_params is None:
      # Allowing init_fn to be called with fast parameters reduces the
      # modifications necessary to adapt code to use lookahead in some cases.
      logging.warning(
          '`params` has no attribute `fast`. Continuing by assuming that '
          'only fast parameters were passed to lookahead init.'
      )
      fast_params = params

    return LookaheadState(
        fast_state=fast_optimizer.init(fast_params),
        steps_since_sync=jnp.zeros(shape=(), dtype=jnp.int32),
    )

  def update_fn(
      updates: base.Updates, state: LookaheadState, params: LookaheadParams
  ) -> tuple[LookaheadParams, LookaheadState]:
    updates, fast_state = fast_optimizer.update(
        updates, state.fast_state, params.fast
    )

    sync_next = state.steps_since_sync == (sync_period - 1)
    updates = _lookahead_update(updates, sync_next, params, slow_step_size)
    if reset_state:
      # Jittable way of resetting the fast optimizer state if parameters will be
      # synchronized after this update step.
      initial_state = fast_optimizer.init(params.fast)
      fast_state = jax.tree.map(
          lambda current, init: (1 - sync_next) * current + sync_next * init,
          fast_state,
          initial_state,
      )

    steps_since_sync = (state.steps_since_sync + 1) % sync_period
    return updates, LookaheadState(fast_state, steps_since_sync)

  return base.GradientTransformation(init_fn, update_fn)

