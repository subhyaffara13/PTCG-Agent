
def optimistic_gradient_descent(
    learning_rate: base.ScalarOrSchedule,
    alpha: base.ScalarOrSchedule = 1.0,
    beta: base.ScalarOrSchedule = 1.0,
) -> base.GradientTransformationExtraArgs:
  r"""An Optimistic Gradient Descent optimizer.

  Optimistic gradient descent is an approximation of extra-gradient methods
  which require multiple gradient calls to compute the next update. It has
  strong formal guarantees for last-iterate convergence in min-max games, for
  which standard gradient descent can oscillate or even diverge.

  At step :math:`t`, the parameters :math:`w_t` are updated according to the
  current gradient :math:`g_t` as well as the previous gradient :math:`g_{t-1}`,
  scaled by the learning rate :math:`\eta_t`:

  .. math::

    \begin{align*}
      u_t &= (\alpha_t + \beta_t) g_t - \beta_t g_{t-1} \\
      w_{t+1} &= w_t - \eta_t u_t
    \end{align*}

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    alpha: Coefficient for generalized OGD.
    beta: Coefficient for generalized OGD negative momentum.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.optimistic_gradient_descent(learning_rate=0.003)
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
    Mokhtari et al, `A Unified Analysis of Extra-gradient and
    Optimistic Gradient Methods for Saddle Point Problems: Proximal
    Point Approach <https://arxiv.org/abs/1901.08511>`_, 2019

  .. seealso::
    :doc:`../_collections/examples/ogda_example`
  """
  return combine.chain(
      transform.scale_by_optimistic_gradient(alpha=alpha, beta=beta),
      transform.scale_by_learning_rate(learning_rate),
  )

