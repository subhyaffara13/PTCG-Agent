
def adabelief(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-16,
    eps_root: jax.typing.ArrayLike = 1e-16,
    *,
    nesterov: bool = False,
) -> base.GradientTransformationExtraArgs:
  r"""The AdaBelief optimizer.

  AdaBelief is an adaptive learning rate optimizer that focuses on fast
  convergence, generalization, and stability. It adapts the step size depending
  on its "belief" in the gradient direction — the optimizer adaptively scales
  the step size by the difference between the predicted and observed gradients.
  AdaBelief is a modified version of :func:`optax.adam` and contains the same
  number of parameters.

  Let :math:`\alpha_t` represent the learning rate and :math:`\beta_1, \beta_2`,
  :math:`\varepsilon`, :math:`\bar{\varepsilon}` represent the arguments
  ``b1``, ``b2``, ``eps`` and ``eps_root`` respectively. The learning rate is
  indexed by :math:`t` since the learning rate may also be provided by a
  schedule function.

  The ``init`` function of this optimizer initializes an internal state
  :math:`S_0 := (m_0, s_0) = (0, 0)`, representing initial estimates for the
  first and second moments. In practice these values are stored as pytrees
  containing all zeros, with the same shape as the model updates.
  At step :math:`t`, the ``update`` function of this optimizer takes as
  arguments the incoming gradients :math:`g_t` and optimizer state :math:`S_t`
  and computes updates :math:`u_t` and new state :math:`S_{t+1}`. Thus, for
  :math:`t > 0`, we have,

  .. math::

    \begin{align*}
      m_t &\leftarrow \beta_1 \cdot m_{t-1} + (1-\beta_1) \cdot g_t \\
      s_t &\leftarrow \beta_2 \cdot s_{t-1} + (1-\beta_2) \cdot (g_t - m_t)^2
      + \bar{\varepsilon} \\
      \hat{m}_t &\leftarrow m_t / {(1-\beta_1^t)} \\
      \hat{s}_t &\leftarrow s_t / {(1-\beta_2^t)} \\
      u_t &\leftarrow -\alpha_t \cdot \hat{m}_t / \left(\sqrt{\hat{s}_t}
      + \varepsilon \right) \\
      S_t &\leftarrow (m_t, s_t).
    \end{align*}

  With the keyword argument `nesterov=True`, the optimizer uses Nesterov
  momentum, replacing the above :math:`\hat{m}_t` with

  .. math::
      \hat{m}_t \leftarrow
        \beta_1 m_t / {(1-\beta_1^{t+1})} + (1 - \beta_1) g_t / {(1-\beta_1^t)}.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate to track the first moment of past gradients.
    b2: Exponential decay rate to track the second moment of past gradients.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the second moment of the prediction error to
      improve numerical stability. If backpropagating gradients through the
      gradient transformation (e.g. for meta-learning), this must be non-zero.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.adabelief(learning_rate=0.003)
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
    Objective function: 1.38E+01

  References:
    Zhuang, `AdaBelief Optimizer: Adapting Stepsizes by the Belief in Observed
    Gradients <https://arxiv.org/abs/2010.07468>`_, 2020

  .. note::
    The default epsilon values in the paper are ``eps=1e-8``, ``eps_root=0.``.
  """
  return combine.chain(
      transform.scale_by_belief(
          b1=b1,
          b2=b2,
          eps=eps,
          eps_root=eps_root,
          nesterov=nesterov,
      ),
      transform.scale_by_learning_rate(learning_rate),
  )

