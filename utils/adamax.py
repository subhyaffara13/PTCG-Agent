
def adamax(
    params: list[Tensor],
    grads: list[Tensor],
    exp_avgs: list[Tensor],
    exp_infs: list[Tensor],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    foreach: bool | None = None,
    maximize: bool = False,
    differentiable: bool = False,
    capturable: bool = False,
    has_complex: bool = False,
    *,
    eps: float,
    beta1: float,
    beta2: float,
    lr: float,
    weight_decay: float,
) -> None:
    r"""Functional API that performs adamax algorithm computation.

    See :class:`~torch.optim.Adamax` for details.
    """

    if not torch.compiler.is_compiling() and not all(
        isinstance(t, torch.Tensor) for t in state_steps
    ):
        raise RuntimeError(
            "API has changed, `state_steps` argument must contain a list of singleton tensors"
        )

    if foreach is None:
        _, foreach = _default_to_fused_or_foreach(
            params, differentiable, use_fused=False
        )

    if foreach and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with foreach optimizers")

    if foreach and not torch.jit.is_scripting():
        func = _multi_tensor_adamax
    else:
        func = _single_tensor_adamax

    func(
        params,
        grads,
        exp_avgs,
        exp_infs,
        state_steps,
        eps=eps,
        beta1=beta1,
        beta2=beta2,
        lr=lr,
        weight_decay=weight_decay,
        maximize=maximize,
        differentiable=differentiable,
        has_complex=has_complex,
        capturable=capturable,
    )


def adamax(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
) -> base.GradientTransformationExtraArgs:
  r"""A variant of the Adam optimizer that uses the infinity norm.

  AdaMax is a variant of the :func:`optax.adam` optimizer. By generalizing
  Adam's :math:`L^2` norm to an :math:`L^p` norm and taking the limit as
  :math:`p \rightarrow \infty`, we obtain a simple and stable update rule.

  Let :math:`\alpha_t` represent the learning rate and :math:`\beta_1, \beta_2`,
  :math:`\varepsilon` represent the arguments
  ``b1``, ``b2`` and ``eps`` respectively. The learning rate is
  indexed by :math:`t` since the learning rate may also be provided by a
  schedule function.

  The ``init`` function of this optimizer initializes an internal state
  :math:`S_0 := (m_0, v_0) = (0, 0)`, representing initial estimates for the
  first and second moments. In practice these values are stored as pytrees
  containing all zeros, with the same shape as the model updates.
  At step :math:`t`, the ``update`` function of this optimizer takes as
  arguments the incoming gradients :math:`g_t` and optimizer state :math:`S_t`
  and computes updates :math:`u_t` and new state :math:`S_{t+1}`. Thus, for
  :math:`t > 0`, we have,

  .. math::

    \begin{align*}
      m_t &\leftarrow \beta_1 \cdot m_{t-1} + (1-\beta_1) \cdot g_t \\
      v_t &\leftarrow \max(\left| g_t \right| + \varepsilon, \beta_2 \cdot
      v_{t-1}) \\
      \hat{m}_t &\leftarrow m_t / (1-\beta_1^t) \\
      u_t &\leftarrow -\alpha_t \cdot \hat{m}_t / v_t \\
      S_t &\leftarrow (m_t, v_t).
    \end{align*}

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate to track the first moment of past gradients.
    b2: Exponential decay rate to track the maximum of past gradients.
    eps: A small constant applied to denominator to avoid dividing by zero when
      rescaling.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.adamax(learning_rate=0.003)
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
    Kingma et al, 2014: https://arxiv.org/abs/1412.6980

  .. seealso:: :func:`optax.adam`, :func:`optax.adamaxw`.
  """
  return combine.chain(
      transform.scale_by_adamax(
          b1=b1,
          b2=b2,
          eps=eps,
      ),
      transform.scale_by_learning_rate(learning_rate),
  )


def adamax(step_size, b1=0.9, b2=0.999, eps=1e-8):
  """Construct optimizer triple for AdaMax (a variant of Adam based on infinity norm).

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.
    b1: optional, a positive scalar value for beta_1, the exponential decay rate
      for the first moment estimates (default 0.9).
    b2: optional, a positive scalar value for beta_2, the exponential decay rate
      for the second moment estimates (default 0.999).
    eps: optional, a positive scalar value for epsilon, a small constant for
      numerical stability (default 1e-8).

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)
  def init(x0):
    m0 = jnp.zeros_like(x0)
    u0 = jnp.zeros_like(x0)
    return x0, m0, u0
  def update(i, g, state):
    x, m, u = state
    m = (1 - b1) * g + b1 * m  # First  moment estimate.
    u = jnp.maximum(b2 * u, jnp.abs(g))  # Update exponentially weighted infinity norm.
    x = (x - (step_size(i) / (1 - jnp.asarray(b1, m.dtype) ** (i + 1))) * m
         / (u + eps))
    return x, m, u
  def get_params(state):
    x, _, _ = state
    return x
  return init, update, get_params

