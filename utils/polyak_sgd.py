
def polyak_sgd(
    max_learning_rate: jax.typing.ArrayLike = 1.0,
    scaling: base.ScalarOrSchedule = 1.0,
    f_min: jax.typing.ArrayLike = 0.0,
    eps: jax.typing.ArrayLike = 0.0,
    variant: str = 'sps',
) -> base.GradientTransformationExtraArgs:
  r"""SGD with Polyak step-size.

  This solver implements the SGD with Polyak step size of (Loizou et al. 2021).
  It sets the step-size as

  .. math::
    s \min\left\{\frac{f(x) - f^\star}{\|\nabla f(x)\|^2 + \epsilon},
      \gamma_{\max}\right\}\,,

  where :math:`f` is the function from which a gradient is computed,
  :math:`\gamma_{\max}` is a maximal acceptable learning rate set  by
  ``max_learning_rate``, :math:`\epsilon` is a constant preventing division by
  zero set with ``eps``, :math:`s` scales the formula by ``scaling``, and
  :math:`f^\star` is a guess of the minimum value of the function set with
  ``f_min``.

  Setting ``variant="sps+"`` (Garrigos et al. 2023) uses only the non-negative
  part of the suboptimality gap. That is, it replaces :math:`f(x) - f^\star`
  with :math:`(f(x) - f^\star)_+`, where :math:`a_+ = \max \{x, 0\}`.

  Args:
    max_learning_rate: a maximum step size to use (defaults to 1).
    scaling: A global scaling factor, either fixed or evolving along iterations
      with a scheduler (defaults to 1).
    f_min: a lower bound on the objective function (defaults to 0). Corresponds
      to :math:`f^\star` in the formula above.
    eps: a value to add in the denominator of the update (defaults to 0).
    variant: either ``'sps'`` or ``'sps+'`` (defaults to ``'sps'``).

  Returns:
    A :class:`optax.GradientTransformationExtraArgs`, where the ``update``
    functiontakes an additional keyword argument ``value`` containing the
    current value of the objective function.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.polyak_sgd()
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  value, grad = jax.value_and_grad(f)(params)
    ...  params, opt_state = solver.update(grad, opt_state, params, value=value)
    ...  print('Objective function: ', f(params))
    Objective function:  3.5
    Objective function:  0.875
    Objective function:  0.21875
    Objective function:  0.0546875
    Objective function:  0.013671875

  References:
    Loizou et al. `Stochastic polyak step-size for SGD: An adaptive learning
    rate for fast convergence <https://arxiv.org/abs/2002.10542>`_, 2021

    Berrada et al., `Training neural networks for and by interpolation
    <https://arxiv.org/pdf/1906.05661.pdf>`_, 2020

    Garrigos et al., `Function value learning: Adaptive learning rates based on
    the Polyak stepsize and function splitting in ERM
    <https://arxiv.org/abs/2307.14528>`_, 2023

  .. warning::
    This method requires knowledge of an approximate value of the
    objective function minimum, passed through the ``f_min`` argument.
    For models that interpolate the data, this can be set to 0 (default
    value).
    Failing to set an appropriate value for ``f_min`` can lead to
    divergence or convergence to a suboptimal solution.
  """
  return combine.chain(
      sgd(learning_rate=scaling),
      transform.scale_by_polyak(
          max_learning_rate=max_learning_rate,
          f_min=f_min,
          eps=eps,
          variant=variant,
      ),
  )

