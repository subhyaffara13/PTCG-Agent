
def radam(
    params: list[Tensor],
    grads: list[Tensor],
    exp_avgs: list[Tensor],
    exp_avg_sqs: list[Tensor],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    decoupled_weight_decay: bool = False,
    foreach: bool | None = None,
    differentiable: bool = False,
    capturable: bool = False,
    has_complex: bool = False,
    maximize: bool = False,
    *,
    beta1: float,
    beta2: float,
    lr: float,
    weight_decay: float,
    eps: float,
) -> None:
    r"""Functional API that performs RAdam algorithm computation.

    See :class:`~torch.optim.RAdam` for details.
    """
    if not all(isinstance(t, torch.Tensor) for t in state_steps):
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
        func = _multi_tensor_radam
    else:
        func = _single_tensor_radam

    func(
        params,
        grads,
        exp_avgs,
        exp_avg_sqs,
        state_steps,
        beta1=beta1,
        beta2=beta2,
        lr=lr,
        weight_decay=weight_decay,
        eps=eps,
        maximize=maximize,
        decoupled_weight_decay=decoupled_weight_decay,
        differentiable=differentiable,
        capturable=capturable,
        has_complex=has_complex,
    )


def radam(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    threshold: jax.typing.ArrayLike = 5.0,
    *,
    nesterov: bool = False,
) -> base.GradientTransformationExtraArgs:
  """The Rectified Adam optimizer.

  The adaptive learning rate in Adam has undesirably large variance in early
  stages of training, due to the limited number of training samples used to
  estimate the optimizer's statistics. Rectified Adam addresses this issue
  by analytically reducing the large variance.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate to track the first moment of past gradients.
    b2: Exponential decay rate to track the second moment of past gradients.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.
    threshold: Threshold for variance tractability.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.radam(learning_rate=0.003)
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
    Liu et al, 2020: `On the Variance of the Adaptive Learning Rate and Beyond
    <https://arxiv.org/abs/1908.03265>`_, 2020
  """
  return combine.chain(
      transform.scale_by_radam(
          b1=b1,
          b2=b2,
          eps=eps,
          eps_root=eps_root,
          threshold=threshold,
          nesterov=nesterov,
      ),
      transform.scale_by_learning_rate(learning_rate),
  )

