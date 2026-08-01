
def fromage(
    learning_rate: base.ScalarOrSchedule, min_norm: jax.typing.ArrayLike = 1e-6
) -> base.GradientTransformationExtraArgs:
  """The Frobenius matched gradient descent (Fromage) optimizer.

  Fromage is a learning algorithm that does not require learning rate tuning.
  The optimizer is based on modeling neural network gradients via deep relative
  trust (a distance function on deep neural networks). Fromage is similar to the
  LARS optimizer and can work on a range of standard neural network benchmarks,
  such as natural language Transformers and generative adversarial networks.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    min_norm: A minimum value that the norm of the gradient updates and the norm
      of the layer parameters can be clipped to to avoid dividing by zero when
      computing the trust ratio (as in the LARS paper).

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.fromage(learning_rate=0.003)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.39E+01
    Objective function: 1.38E+01
    Objective function: 1.37E+01
    Objective function: 1.37E+01
    Objective function: 1.36E+01

  References:
    Bernstein et al, `On the distance between two neural networks and the
    stability of learning <https://arxiv.org/abs/2002.03432>`_, 2020
  """
  if not callable(learning_rate):
    mult = 1 / (1 + learning_rate**2)**0.5
    return combine.chain(
        transform.scale_by_trust_ratio(min_norm),
        transform.scale_by_learning_rate(learning_rate * mult),
        transform.add_decayed_weights((mult - 1)),
    )
  else:
    mult_lr = lambda count: 1 / (1 + learning_rate(count)**2)**0.5
    return combine.chain(
        transform.scale_by_trust_ratio(min_norm),
        transform.scale_by_learning_rate(
            lambda c: mult_lr(c) * learning_rate(c)),
        transform.add_decayed_weights(lambda c: mult_lr(c) - 1),
    )

