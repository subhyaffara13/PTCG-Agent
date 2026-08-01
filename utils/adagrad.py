
def adagrad(
    params: list[Tensor],
    grads: list[Tensor],
    state_sums: list[Tensor],
    state_steps: list[Tensor],
    fused: bool | None = None,
    grad_scale: Tensor | None = None,
    found_inf: Tensor | None = None,
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting these as kwargs for now as functional API is compiled by torch/distributed/optim
    has_sparse_grad: bool = False,
    foreach: bool | None = None,
    differentiable: bool = False,
    has_complex: bool = False,
    *,
    lr: float,
    weight_decay: float,
    lr_decay: float,
    eps: float,
    maximize: bool,
) -> None:
    r"""Functional API that performs Adagrad algorithm computation.

    See :class:`~torch.optim.Adagrad` for details.
    """
    if not all(isinstance(t, torch.Tensor) for t in state_steps):
        raise RuntimeError(
            "API has changed, `state_steps` argument must contain a list of singleton tensors"
        )

    # Respect when the user inputs False/True for foreach or fused. We only want to change
    # the default when neither have been user-specified. Note that we default to foreach
    # and pass False to use_fused. This is not a mistake--we want to give the fused impl
    # bake-in time before making it the default, even if it is typically faster.
    if fused is None and foreach is None:
        _, foreach = _default_to_fused_or_foreach(
            params, differentiable, use_fused=False
        )

    if fused is None:
        fused = False
    if foreach is None:
        foreach = False

    if foreach and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with foreach optimizers")
    if fused and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with fused optimizers")

    if fused and not torch.jit.is_scripting():
        func = _fused_adagrad
    elif foreach and not torch.jit.is_scripting():
        func = _multi_tensor_adagrad
    else:
        func = _single_tensor_adagrad

    func(
        params,
        grads,
        state_sums,
        state_steps,
        lr=lr,
        weight_decay=weight_decay,
        lr_decay=lr_decay,
        eps=eps,
        has_sparse_grad=has_sparse_grad,
        maximize=maximize,
        differentiable=differentiable,
        has_complex=has_complex,
        grad_scale=grad_scale,
        found_inf=found_inf,
    )


def adagrad(
    learning_rate: base.ScalarOrSchedule,
    initial_accumulator_value: jax.typing.ArrayLike = 0.1,
    eps: jax.typing.ArrayLike = 1e-7,
) -> base.GradientTransformationExtraArgs:
  r"""The Adagrad optimizer.

  AdaGrad is a sub-gradient algorithm for stochastic optimization that adapts
  the learning rate individually for each feature based on its gradient history.

  The updated parameters adopt the form:

      .. math::

        w_{t+1}^{(i)} = w_{t}^{(i)} - \eta \frac{g_{t}^{(i)}}
                     {\sqrt{\sum_{\tau=1}^{t} (g_{\tau}^{(i)})^2 + \epsilon}}

  where:
    - :math:`w_t^{(i)}` is the parameter :math:`i` at time step :math:`t`,
    - :math:`\eta` is the learning rate,
    - :math:`g_t^{(i)}` is the gradient of parameter :math:`i` at time step
      :math:`t`,
    - :math:`\epsilon` is a small constant to ensure numerical stability.

  Defining :math:`G = \sum_{t=1}^\tau g_t g_t^\top`, the update can be
  written as

      .. math::

          w_{t+1} = w_{t} - \eta \cdot \text{diag}(G + \epsilon I)^{-1/2}
          \cdot g_t

  where :math:`\text{diag} (G) = (G_{ii})_{i=1}^p` is the vector of diagonal
  entries of :math:`G \in \mathbb{R}^p` and :math:`I` is the identity matrix
  in :math:`\mathbb{R}^p`.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    initial_accumulator_value: Initial value for the accumulator.
    eps: A small constant applied to denominator inside of the square root (as
      in RMSProp) to avoid dividing by zero when rescaling.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.adagrad(learning_rate=1.0)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 5.01E+00
    Objective function: 2.40E+00
    Objective function: 1.25E+00
    Objective function: 6.86E-01
    Objective function: 3.85E-01

  References:
    Duchi et al, `Adaptive Subgradient Methods for Online Learning and
    Stochastic Optimization <https://jmlr.org/papers/v12/duchi11a.html>`_,
    2011

  .. warning::
    Adagrad's main limit is the monotonic accumulation of squared
    gradients in the denominator: since all terms are >0, the sum keeps growing
    during training and the learning rate eventually becomes vanishingly small.
  """
  return combine.chain(
      transform.scale_by_rss(
          initial_accumulator_value=initial_accumulator_value, eps=eps
      ),
      transform.scale_by_learning_rate(learning_rate),
  )


def adagrad(step_size, momentum=0.9):
  """Construct optimizer triple for Adagrad.

  Adaptive Subgradient Methods for Online Learning and Stochastic Optimization:
  http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.
    momentum: optional, a positive scalar value for momentum

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)

  def init(x0):
    g_sq = jnp.zeros_like(x0)
    m = jnp.zeros_like(x0)
    return x0, g_sq, m

  def update(i, g, state):
    x, g_sq, m = state
    g_sq += jnp.square(g)
    g_sq_inv_sqrt = jnp.where(g_sq > 0, 1. / jnp.sqrt(g_sq), 0.0)
    m = (1. - momentum) * (g * g_sq_inv_sqrt) + momentum * m
    x = x - step_size(i) * m
    return x, g_sq, m

  def get_params(state):
    x, _, _ = state
    return x

  return init, update, get_params

