
def noisy_sgd(
    learning_rate: base.ScalarOrSchedule,
    eta: jax.typing.ArrayLike = 0.01,
    gamma: jax.typing.ArrayLike = 0.55,
    key: jax.typing.ArrayLike | None = None,  # int
    *,
    seed: int | None = None,  # deprecated
) -> base.GradientTransformationExtraArgs:
  r"""A variant of SGD with added noise.

  Noisy SGD is a variant of :func:`optax.sgd` that incorporates Gaussian noise
  into the updates. It has been found that adding noise to the gradients can
  improve both the training error and the generalization error in very deep
  networks.

  The update :math:`u_t` is modified to include this noise as follows:

  .. math::
    u_t \leftarrow -\alpha_t (g_t + N(0, \sigma_t^2)),

  where :math:`N(0, \sigma_t^2)` represents Gaussian noise with zero mean and a
  variance of :math:`\sigma_t^2`.

  The variance of this noise decays over time according to the formula

  .. math::
    \sigma_t^2 = \frac{\eta}{(1+t)^\gamma},

  where :math:`\gamma` is the decay rate parameter ``gamma`` and :math:`\eta`
  represents the initial variance ``eta``.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    eta: Initial variance for the Gaussian noise added to gradients.
    gamma: A parameter controlling the annealing of noise over time ``t``, the
      variance decays according to ``(1+t)**(-gamma)``.
    key: random generator key for noise generation.
    seed: deprecated, use key instead.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.noisy_sgd(learning_rate=0.003, key=0)
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
  return combine.chain(
      transform.add_noise(eta, gamma, key, seed=seed),
      transform.scale_by_learning_rate(learning_rate),
  )

