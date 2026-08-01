
def novograd(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.25,
    eps: jax.typing.ArrayLike = 1e-6,
    eps_root: jax.typing.ArrayLike = 0.0,
    weight_decay: base.ScalarOrSchedule = 0.0,
) -> base.GradientTransformationExtraArgs:
  """NovoGrad optimizer.

  NovoGrad is more robust to the initial learning rate and
  weight initialization than other methods. For example,
  NovoGrad works well without LR warm-up, while other methods require it.
  NovoGrad performs exceptionally well for large batch training, e.g. it
  outperforms other methods for ResNet-50 for all batches up to 32K.
  In addition, NovoGrad requires half the memory compared to Adam.
  It was introduced together with Jasper ASR model.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: An exponential decay rate to track the first moment of past gradients.
    b2: An exponential decay rate to track the second moment of past gradients.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.
    weight_decay: Strength of the weight decay regularization.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.novograd(learning_rate=0.003)
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
    Objective function: 1.38E+01
    Objective function: 1.37E+01

  References:
    Ginsburg et al, `Stochastic Gradient Methods with Layer-wise Adaptive
    Moments for Training of Deep Networks <https://arxiv.org/abs/1905.11286>`_,
    2019

    Li et al, `Jasper: An End-to-End Convolutional Neural Acoustic Model
    <https://arxiv.org/abs/1904.03288>`_, 2019
  """
  return combine.chain(
      transform.scale_by_novograd(
          b1=b1, b2=b2, eps=eps, eps_root=eps_root, weight_decay=weight_decay
      ),
      transform.scale_by_learning_rate(learning_rate),
  )

