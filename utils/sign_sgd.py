
def sign_sgd(
    learning_rate: base.ScalarOrSchedule,
) -> base.GradientTransformationExtraArgs:
  r"""A variant of SGD using only the signs of the gradient components.

  SignSGD is a variant of SGD that uses the signs of the gradient components in
  the update, not their actual values. The update :math:`u_t` is modified as
  follows:

  .. math::
    u_t \leftarrow -\alpha_t\, \text{sign}\,(g_t),

  for :math:`\alpha_t` a given learning rate at iteration :math:`t`, and
  :math:`\text{sign}\,(g_t)` the sign of each component of the gradient
  :math:`g_t`.

  SGD variants that use only the signs of the gradient update have historically
  been used since RProp, with modern forms including RMSProp, Adam, and Lion.
  SignSGD uses only the signs of the gradient update. SignSGD enables
  significant gradient compression, substantially reducing the bottleneck
  imposed by communicating gradients when distributing learning across multiple
  workers.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.sign_sgd(learning_rate=0.003)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.40E+01
    Objective function: 1.39E+01
    Objective function: 1.39E+01
    Objective function: 1.39E+01
    Objective function: 1.38E+01

  References:
    Bernstein et al., `signSGD: Compressed optimization for Non-Convex Problems
    <https://arxiv.org/abs/1802.04434>`_, 2018

    Balles et al., `The Geometry of Sign Gradient Descent
    <https://arxiv.org/abs/2002.08056>`_, 2020
  """
  return combine.chain(
      transform.scale_by_sign(),
      transform.scale_by_learning_rate(learning_rate),
  )

