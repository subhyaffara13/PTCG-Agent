
def optimistic_adam(
    learning_rate: jax.typing.ArrayLike,
    optimism: Optional[jax.typing.ArrayLike] = None,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-08,
    eps_root: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[Any] = None,
    *,
    nesterov: bool = True,
) -> base.GradientTransformationExtraArgs:
  r"""The Optimistic Adam optimizer.

  This is an optimistic version of the Adam optimizer. It addresses the issue
  of limit cycling behavior in training Generative Adversarial Networks and
  other saddle-point min-max problems.

  The algorithm is as follows. First, we define the following parameters:

  - :math:`\alpha`: the learning rate.
  - :math:`o` the optimism rate.
  - :math:`\beta_1` the exponential decay rate for the first moment estimate.
  - :math:`\beta_2` the exponential decay rate for the second moment estimate.

  Second, we define the following variables:

  - :math:`g_t`: the incoming gradient.
  - :math:`m_t`: the biased first moment estimate.
  - :math:`v_t`: the biased second raw moment estimate.
  - :math:`\hat{m}_t`: the bias-corrected first moment estimate.
  - :math:`\hat{v}_t`: the bias-corrected second raw moment estimate.
  - :math:`r_t`: the signal-to-noise ratio (SNR) vector.
  - :math:`u_t`: the outgoing update vector.
  - :math:`S_t`: the state of the optimizer.

  Finally, on each iteration, the variables are updated as follows:

  .. math::

    \begin{align*}
      m_t &\leftarrow \beta_1 \cdot m_{t - 1} + (1 - \beta_1) \cdot g_t \\
      v_t &\leftarrow \beta_2 \cdot v_{t - 1} + (1 - \beta_2) \cdot g_t^2 \\
      \hat{m}_t &\leftarrow m_t / {(1 - \beta_1^t)} \\
      \hat{v}_t &\leftarrow v_t / {(1 - \beta_2^t)} \\
      r_t &\leftarrow \hat{m}_t / \left({\sqrt{\hat{v}_t +
        \bar{\varepsilon}} + \varepsilon} \right) \\
      u_t &\leftarrow -\alpha r_t - o (r_t - r_{t - 1}) \\
      S_t &\leftarrow (m_t, v_t, r_t).
    \end{align*}

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    optimism: The amount of optimism to be applied. If None, defaults to
      learning_rate, as in the paper.
    b1: Exponential decay rate to track the first moment of past gradients.
    b2: Exponential decay rate to track the second moment of past gradients.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the second moment of the prediction error to
      improve numerical stability. If backpropagating gradients through the
      gradient transformation (e.g. for meta-learning), this must be non-zero.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> from jax import numpy as jnp, lax
    >>> def f(x, y):
    ...  return x * y  # simple bilinear function
    >>> opt = optax.optimistic_adam(1e-2, 1.0)
    >>> def step(state, _):
    ...  params, opt_state = state
    ...  distance = jnp.hypot(*params)
    ...  grads = jax.grad(f, argnums=(0, 1))(*params)
    ...  grads = grads[0], -grads[1]
    ...  updates, opt_state = opt.update(grads, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  return (params, opt_state), distance
    >>> params = 1.0, 2.0
    >>> opt_state = opt.init(params)
    >>> _, distances = lax.scan(step, (params, opt_state), length=1025)
    >>> for i in range(6):
    ...  print(f"{distances[4**i]:.3f}")
    2.243
    2.195
    2.161
    2.055
    0.796
    0.001

  References:
    Daskalakis et al, `Training GANs with Optimism
    <https://arxiv.org/abs/1711.00141>`_, 2017

  .. seealso::
    :doc:`../_collections/examples/ogda_example`
  """
  warnings.warn('`optimistic_adam` is deprecated, please use'
                ' `optimistic_adam_v2` instead.', category=DeprecationWarning)
  if callable(learning_rate):
    raise ValueError('This version of `optimistic_adam` does not support'
                     ' learning rate schedules but `optimistic_adam_v2` does.')
  if optimism is None:
    optimism = learning_rate
  return combine.chain(
      transform.scale_by_adam(
          b1=b1,
          b2=b2,
          eps=eps,
          eps_root=eps_root,
          mu_dtype=mu_dtype,
          nesterov=nesterov,
      ),
      transform.scale_by_optimistic_gradient(alpha=learning_rate,
                                             beta=optimism),
      transform.scale_by_learning_rate(1.0),  # flips the sign
  )

