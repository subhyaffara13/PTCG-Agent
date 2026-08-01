
def add_noise(
    eta: jax.typing.ArrayLike,
    gamma: jax.typing.ArrayLike,
    key: jax.Array | int | None = None,
    *,
    seed: int | None = None,  # deprecated
) -> base.GradientTransformation:
  """Add gradient noise.

  Args:
    eta: Base variance of the gaussian noise added to the gradient.
    gamma: Decay exponent for annealing of the variance.
    key: random generator key for noise generation.
    seed: deprecated, use key instead.

  Returns:
    A :class:`optax.GradientTransformation` object.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> key = jax.random.key(0)  # could also be key=0
    >>> noise = optax.add_noise(eta=0.01, gamma=0.55, key=key)
    >>> sgd = optax.scale_by_learning_rate(learning_rate=0.003)
    >>> solver = optax.chain(noise, sgd)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.38E+01
    Objective function: 1.37E+01
    Objective function: 1.35E+01
    Objective function: 1.33E+01
    Objective function: 1.32E+01

  References:
    Neelakantan et al, `Adding Gradient Noise Improves Learning for Very Deep
    Networks <https://arxiv.org/abs/1511.06807>`_, 2015
  """

  if seed is not None:
    warnings.warn(
        '"seed" is deprecated and will be removed in optax 0.2.7, use "key".',
        DeprecationWarning,
    )
    if key is not None:
      raise ValueError('Only one of seed or key can be specified.')
    key = seed
  if key is None:
    warnings.warn('Specifying a key will be required in optax 0.2.7.')
    key = 0

  def init_fn(params):
    del params
    return AddNoiseState(
        count=jnp.zeros([], jnp.int32), rng_key=utils.canonicalize_key(key)
    )

  def update_fn(updates, state, params=None):
    del params
    count_inc = numerics.safe_increment(state.count)
    standard_deviation = jnp.sqrt(eta / count_inc**gamma)

    rng_key, sample_key = jax.random.split(state.rng_key)
    noise = optax.tree.random_like(
        sample_key, target_tree=updates, sampler=jax.random.normal
    )
    updates = optax.tree.add_scale(
        tree_x=updates, scalar=standard_deviation, tree_y=noise
    )
    return updates, AddNoiseState(count=count_inc, rng_key=rng_key)

  return base.GradientTransformation(init_fn, update_fn)

