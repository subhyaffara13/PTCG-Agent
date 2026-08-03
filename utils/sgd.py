from typing import Any, Optional

def sgd(
    params: list[Tensor],
    d_p_list: list[Tensor],
    momentum_buffer_list: list[Tensor | None],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    has_sparse_grad: bool = False,
    foreach: bool | None = None,
    fused: bool | None = None,
    grad_scale: Tensor | None = None,
    found_inf: Tensor | None = None,
    *,
    weight_decay: float,
    momentum: float,
    lr: float,
    dampening: float,
    nesterov: bool,
    maximize: bool,
) -> None:
    r"""Functional API that performs SGD algorithm computation.

    See :class:`~torch.optim.SGD` for details.
    """
    # Respect when the user inputs False/True for foreach or fused. We only want to change
    # the default when neither have been user-specified. Note that we default to foreach
    # and pass False to use_fused. This is not a mistake--we want to give the fused impl
    # bake-in time before making it the default, even if it is typically faster.
    if foreach is None and fused is None:
        # why must we be explicit about an if statement for torch.jit.is_scripting here?
        # because JIT can't handle Optionals nor fancy conditionals when scripting
        if not torch.jit.is_scripting():
            fused, foreach = _default_to_fused_or_foreach(
                params, differentiable=False, use_fused=False
            )
        else:
            foreach = False
            fused = False
    if foreach is None:
        foreach = False
    if fused is None:
        fused = False

    if foreach and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with foreach optimizers")
    if fused and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with fused optimizers")

    if foreach and not torch.jit.is_scripting():
        func = _multi_tensor_sgd
    elif fused and not torch.jit.is_scripting():
        func = _fused_sgd
    else:
        func = _single_tensor_sgd

    func(
        params,
        d_p_list,
        momentum_buffer_list,
        weight_decay=weight_decay,
        momentum=momentum,
        lr=lr,
        dampening=dampening,
        nesterov=nesterov,
        has_sparse_grad=has_sparse_grad,
        maximize=maximize,
        grad_scale=grad_scale,
        found_inf=found_inf,
    )


def sgd(
    learning_rate: base.ScalarOrSchedule,
    momentum: Optional[jax.typing.ArrayLike] = None,
    nesterov: bool = False,
    accumulator_dtype: Optional[Any] = None,
) -> base.GradientTransformationExtraArgs:
  r"""A canonical Stochastic Gradient Descent optimizer.

  This implements stochastic gradient descent. It also includes support for
  momentum, and Nesterov acceleration, as these are standard practice when
  using stochastic gradient descent to train deep neural networks.


  The canonical stochastic gradient descent returns an update
  :math:`u_t` of the form

  .. math::
    u_t \leftarrow -\alpha_t g_t,

  where :math:`g_t` is the gradient of the objective (potentially preprocessed
  by other transformations) and :math:`\alpha_t` is the ``learning_rate`` at
  time :math:`t` (constant or selected by an :class:`optax.Schedule`).

  Stochastic gradient descent with momentum takes two possible forms.

  .. math::

    \begin{align*}
      m_t &\leftarrow g_t + \mu m_{t-1} \\
      u_t &\leftarrow \begin{cases}
        -\alpha_t m_t & \text{ if } \texttt{nesterov = False} \\
        -\alpha_t (g_t + \mu m_t) & \text{ if } \texttt{nesterov = True}
        \end{cases} \\
      S_t &\leftarrow m_t,
    \end{align*}

  where :math:`\mu` is the ``momentum`` parameter and :math:`S_t` is the state
  of the optimizer.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    momentum: Decay rate used by the momentum term, when it is set to ``None``,
      then momentum is not used at all.
    nesterov: Whether Nesterov momentum is used.
    accumulator_dtype: Optional ``dtype`` to be used for the accumulator; if
      ``None`` then the ``dtype`` is inferred from ``params`` and ``updates``.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.sgd(learning_rate=0.003)
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
    Sutskever et al, `On the importance of initialization and momentum in deep
    learning <http://proceedings.mlr.press/v28/sutskever13.pdf>`_, 2013
  """
  if momentum is not None:
    opt = transform.trace(
        decay=momentum,
        nesterov=nesterov,
        accumulator_dtype=accumulator_dtype,
    )
  else:
    opt = base.identity()
  return combine.chain(
      opt,
      transform.scale_by_learning_rate(learning_rate),
  )


def sgd(step_size):
  """Construct optimizer triple for stochastic gradient descent.

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)
  def init(x0):
    return x0
  def update(i, g, x):
    return x - step_size(i) * g
  def get_params(x):
    return x
  return Optimizer(init, update, get_params)

