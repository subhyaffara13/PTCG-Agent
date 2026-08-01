
def rmsprop(
    params: list[Tensor],
    grads: list[Tensor],
    square_avgs: list[Tensor],
    grad_avgs: list[Tensor],
    momentum_buffer_list: list[Tensor],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    foreach: bool | None = None,
    maximize: bool = False,
    differentiable: bool = False,
    capturable: bool = False,
    has_complex: bool = False,
    *,
    lr: float,
    alpha: float,
    eps: float,
    weight_decay: float,
    momentum: float,
    centered: bool,
) -> None:
    r"""Functional API that performs rmsprop algorithm computation.

    See :class:`~torch.optim.RMSProp` for details.
    """
    # this check is slow during compilation, so we skip it
    # if it's strictly needed we can add this check back in dynamo
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
        func = _multi_tensor_rmsprop
    else:
        func = _single_tensor_rmsprop

    func(
        params,
        grads,
        square_avgs,
        grad_avgs,
        momentum_buffer_list,
        state_steps,
        lr=lr,
        alpha=alpha,
        eps=eps,
        weight_decay=weight_decay,
        momentum=momentum,
        centered=centered,
        maximize=maximize,
        capturable=capturable,
        differentiable=differentiable,
        has_complex=has_complex,
    )


def rmsprop(
    learning_rate: base.ScalarOrSchedule,
    decay: jax.typing.ArrayLike = 0.9,
    eps: jax.typing.ArrayLike = 1e-8,
    initial_scale: jax.typing.ArrayLike = 0.0,
    eps_in_sqrt: bool = True,
    centered: bool = False,
    momentum: Optional[jax.typing.ArrayLike] = None,
    nesterov: bool = False,
    bias_correction: bool = False,
) -> base.GradientTransformationExtraArgs:
  r"""A flexible RMSProp optimizer.

  RMSProp is an SGD variant with learning rate adaptation. The `learning_rate`
  used for each weight is scaled by a suitable estimate of the magnitude of the
  gradients on previous steps. Several variants of RMSProp can be found
  in the literature. This alias provides an easy to configure RMSProp
  optimizer that can be used to switch between several of these variants.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    decay: Decay used to track the magnitude of previous gradients.
    eps: A small numerical constant to avoid dividing by zero when rescaling.
    initial_scale: Initial value of accumulators tracking the magnitude of
      previous updates. PyTorch uses `0`, TF1 uses `1`. When reproducing results
      from a paper, verify the value used by the authors.
    eps_in_sqrt: Whether to add ``eps`` in the square root of the denominator or
      outside the square root.
    centered: Whether the second moment or the variance of the past gradients is
      used to rescale the latest gradients.
    momentum: Decay rate used by the momentum term, when it is set to `None`,
      then momentum is not used at all.
    nesterov: Whether Nesterov momentum is used.
    bias_correction: Whether to apply bias correction to the estimates of the
      second moments (and first moment if ``centered=True``).

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.rmsprop(learning_rate=0.003)
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
    Hinton, `Overview of mini-batch gradient descent`
    <www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf>`_, 2012

    Graves, `Generating Sequences With Recurrent Neural Networks
    <https://arxiv.org/pdf/1308.0850v5>`_, 2014

    Ziyin, `LaProp: Separating Momentum and Adaptivity in Adam
    <https://arxiv.org/pdf/2002.04839>`_, 2021

  .. warning::
    Default behavior of optax's RMSprop (``eps_in_sqrt=True``) differs from
    Pytorch's implementation and could impact performance.
    If ``eps_in_sqrt=True``, in the denominator, optax uses
    :math:`\sqrt{v + \epsilon}` in the denominator whereas PyTorch uses
    :math:`\sqrt{v} + \epsilon`.
    Using ``eps_in_sqrt=False`` in optax will match PyTorch's behavior.
    See
    https://github.com/google-deepmind/optax/issues/532 for more detail.
  """
  if centered:
    return combine.chain(
        transform.scale_by_stddev(
            decay=decay,
            eps=eps,
            initial_scale=initial_scale,
            eps_in_sqrt=eps_in_sqrt,
            bias_correction=bias_correction,
        ),
        transform.scale_by_learning_rate(learning_rate),
        (
            transform.trace(decay=momentum, nesterov=nesterov)
            if momentum is not None
            else base.identity()
        ),
    )
  return combine.chain(
      transform.scale_by_rms(
          decay=decay,
          eps=eps,
          initial_scale=initial_scale,
          eps_in_sqrt=eps_in_sqrt,
          bias_correction=bias_correction,
      ),
      transform.scale_by_learning_rate(learning_rate),
      (
          transform.trace(decay=momentum, nesterov=nesterov)
          if momentum is not None
          else base.identity()
      ),
  )


def rmsprop(step_size, gamma=0.9, eps=1e-8):
  """Construct optimizer triple for RMSProp.

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to a positive scalar.
      gamma: Decay parameter.
      eps: Epsilon parameter.

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)
  def init(x0):
    avg_sq_grad = jnp.zeros_like(x0)
    return x0, avg_sq_grad
  def update(i, g, state):
    x, avg_sq_grad = state
    avg_sq_grad = avg_sq_grad * gamma + jnp.square(g) * (1. - gamma)
    x = x - step_size(i) * g / jnp.sqrt(avg_sq_grad + eps)
    return x, avg_sq_grad
  def get_params(state):
    x, _ = state
    return x
  return init, update, get_params

