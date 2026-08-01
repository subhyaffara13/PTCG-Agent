
def sam(
    optimizer: base.GradientTransformation,
    adv_optimizer: base.GradientTransformation,
    sync_period: int = 2,
    reset_state: bool = True,
    opaque_mode: bool = False,
    batch_axis_name: Optional[str] = None,
) -> base.GradientTransformationExtraArgs:
  """Implementation of SAM (Sharpness Aware Minimization).

  Performs steps with the inner adversarial optimizer and periodically
  updates an outer set of true parameters.  By default, resets
  the state of the adversarial optimizer after synchronization.  For example::

    >>> import optax
    >>> rho = 0.1
    >>> opt = optax.sgd(learning_rate=0.01)
    >>> adv_opt = optax.chain(optax.contrib.normalize(), optax.sgd(rho))
    >>> sam_opt = optax.contrib.sam(opt, adv_opt, sync_period=2)

  Would implement the simple drop-in SAM version from the paper which uses
  an inner adversarial optimizer of a normalized sgd for one step.

  Args:
    optimizer: the outer optimizer.
    adv_optimizer: the inner adversarial optimizer.
    sync_period: how often to run the outer optimizer, defaults to 2, or every
      other step.
    reset_state: whether to reset the state of the inner optimizer after every
      sync period, defaults to ``True``.
    opaque_mode: bool. If ``True``, the outer optimizer and the adversarial
      optimizer are run in an internal loop at each call to ``update``, so that
      adversarial updates are opaque to the rest of the system. If ``False``,
      one optimizer is (effectively) evaluated per call to ``update``, meaning
      that adversarial updates are visible to the rest of the system. Setting
      ``opaque_mode`` to ``True`` is necessary if the training system using SAM
      has side effects from each call to ``update`` besides the changes to the
      model's parameters. The most common example would be if the model uses
      BatchNorm statistics -- those statistics would be updated on both
      adversarial and non-adversarial update steps, causing them to get out of
      sync with the model's parameters (which are effectively only updated on
      non-adversarial steps). See the NOTE section for more details on
      ``opaque_mode=True``.
    batch_axis_name: str or None. Only used if ``opaque_mode=True``. When
      running in a pmapped setting, it is necessary to take a ``jax.lax.pmean``
      of the adversarial updates internally before passing them to the outer
      optimizer. You only need to specify this if you have to use
      ``jax.lax.pmean`` in your training loop.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`
    implementation of SAM.

  References:
    Foret et al., `Sharpness-Aware Minimization for Efficiently Improving
    Generalization <https://arxiv.org/abs/2010.01412>`_, 2021

  .. note::
    When ``opaque_mode=True``, the ``update`` function must be called with a
    gradient function that takes two arguments (the params and the current
    adversarial step) and returns the gradients of the loss. This looks like
    the following::

      opt = sam(outer_opt, adv_opt, opaque_mode=True)
      ...
      # In the training loop:
      grad_fn = jax.grad(
        lambda params, _: loss(params, batch, and_other_args))
      updates, state = opt.update(updates, state, params, grad_fn=grad_fn)
      params = optax.apply_updates(params, updates)

    On every call to ``opt.update``, ``grad_fn`` will be called
    ``sync_period - 1`` times, once for each adversarial update. It is usually
    ok to use the same minibatch in each of those updates, as in the example
    above, but you can use the second argument to select different batches
    at each adversarial step::

      grad_fn = jax.grad(lambda params, i: loss(params, batches[i]))
  """

  if sync_period < 1:
    raise ValueError("Synchronization period must be >= 1.")

  def init_fn(params: base.Params) -> SAMState:
    return SAMState(
        steps_since_sync=jnp.zeros(shape=(), dtype=jnp.int32),
        opt_state=optimizer.init(params),
        adv_state=adv_optimizer.init(params),
        cache=None if opaque_mode else params,
    )

  def pick_one(cond, if_true, if_false):
    return jax.tree.map(
        lambda if_t, if_f: cond * if_t + (1 - cond) * if_f, if_true, if_false
    )

  def transparent_update_fn(
      updates: base.Updates,
      state: SAMState,
      params: Optional[base.Params],
      *,
      grad_fn: Optional[Callable[[base.Params, int], base.Updates]] = None,
  ) -> tuple[base.Updates, SAMState]:
    del grad_fn
    first_step = state.steps_since_sync == 0
    last_step = state.steps_since_sync == sync_period - 1

    adv_updates, adv_state = adv_optimizer.update(
        updates, state.adv_state, params
    )
    adv_updates = jax.tree.map(lambda x: -x, adv_updates)

    opt_updates, opt_state = optimizer.update(
        updates, state.opt_state, state.cache
    )
    opt_updates = jax.tree.map(
        lambda c, p, u: c - p + u, state.cache, params, opt_updates
    )

    cache = pick_one(first_step, params, state.cache)
    updates = pick_one(last_step, opt_updates, adv_updates)

    if reset_state:
      initial_state = adv_optimizer.init(params)
      adv_state = pick_one(last_step, initial_state, adv_state)
    else:
      adv_state = pick_one(last_step, state.adv_state, adv_state)

    opt_state = pick_one(last_step, opt_state, state.opt_state)

    steps_since_sync = (state.steps_since_sync + 1) % sync_period
    return updates, SAMState(
        steps_since_sync=steps_since_sync,
        adv_state=adv_state,
        opt_state=opt_state,
        cache=cache,
    )

  def opaque_update_fn(
      updates: base.Updates,
      state: SAMState,
      params: Optional[base.Params],
      *,
      grad_fn: Optional[Callable[[base.Params, int], base.Updates]] = None,
  ) -> tuple[base.Updates, SAMState]:
    if grad_fn is None:
      raise ValueError("grad_fn must be provided when opaque_mode=True.")

    outer_params = params
    adv_params = params
    adv_updates = updates
    adv_state = state.adv_state
    for i in range(sync_period - 1):
      adv_updates, adv_state = adv_optimizer.update(
          adv_updates, adv_state, adv_params
      )
      adv_updates = jax.tree.map(lambda x: -x, adv_updates)

      adv_params = update.apply_updates(adv_params, adv_updates)
      adv_updates = grad_fn(adv_params, i)
      if batch_axis_name is not None:
        adv_updates = jax.lax.pmean(adv_updates, axis_name=batch_axis_name)

    if reset_state:
      adv_state = adv_optimizer.init(outer_params)

    updates, opt_state = optimizer.update(
        adv_updates, state.opt_state, outer_params
    )

    return updates, SAMState(
        steps_since_sync=jnp.zeros(shape=(), dtype=jnp.int32),
        adv_state=adv_state,
        opt_state=opt_state,
        cache=None,
    )

  if opaque_mode:
    update_fn = opaque_update_fn
  else:
    update_fn = transparent_update_fn

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

