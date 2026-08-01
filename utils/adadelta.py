
def adadelta(
    params: list[Tensor],
    grads: list[Tensor],
    square_avgs: list[Tensor],
    acc_deltas: list[Tensor],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    capturable: bool = False,
    foreach: bool | None = None,
    differentiable: bool = False,
    has_complex: bool = False,
    *,
    lr: float,
    rho: float,
    eps: float,
    weight_decay: float,
    maximize: bool,
) -> None:
    r"""Functional API that performs Adadelta algorithm computation.

    See :class:`~torch.optim.Adadelta` for details.
    """

    # this check is slow during compilation, so we skip it
    # if it's strictly needed we can add this check back in dynamo
    if not torch.compiler.is_compiling() and not all(
        isinstance(t, torch.Tensor) for t in state_steps
    ):
        raise RuntimeError(
            "API has changed, `state_steps` argument must contain a list of singleton tensors"
        )

    # We still respect when the user inputs False for foreach.
    if foreach is None:
        _, foreach = _default_to_fused_or_foreach(
            params, differentiable, use_fused=False
        )

    if foreach and torch.jit.is_scripting():
        raise RuntimeError("torch.jit.script not supported with foreach optimizers")

    if foreach and not torch.jit.is_scripting():
        func = _multi_tensor_adadelta
    else:
        func = _single_tensor_adadelta

    func(
        params,
        grads,
        square_avgs,
        acc_deltas,
        state_steps,
        lr=lr,
        rho=rho,
        eps=eps,
        weight_decay=weight_decay,
        maximize=maximize,
        differentiable=differentiable,
        capturable=capturable,
        has_complex=has_complex,
    )


def adadelta(
    learning_rate: Optional[base.ScalarOrSchedule] = None,
    rho: jax.typing.ArrayLike = 0.9,
    eps: jax.typing.ArrayLike = 1e-6,
    weight_decay: Union[jax.typing.ArrayLike, base.ScalarOrSchedule] = 0.0,
    weight_decay_mask: MaskOrFn = None,
) -> base.GradientTransformationExtraArgs:
  r"""The Adadelta optimizer.

  Adadelta is a stochastic gradient descent method that adapts learning rates
  based on a moving window of gradient updates. Adadelta is a modification of
  Adagrad.
  It addresses the diminishing learning rates problem in Adagrad by maintaining running averages of squared
  gradients.

  The weight update :math:`\Delta w_t` for this optimizer is given as follows:

  .. math::
      \begin{align*}

      &E[g^2]_t = \rho \cdot E[g^2]_{t-1} + (1-\rho) \cdot g_t^2 \\
      &\Delta w_t = -\frac{\sqrt{E[\Delta w^2]_{t-1} + \epsilon}}{\sqrt{E[g^2]_t + \epsilon}} \cdot g_t

      \end{align*}



  where:
    - :math:`g_t` is the gradient at time step :math:`t`,
    - :math:`E[g^2]_t` is the running average of squared gradients,
    - :math:`E[\Delta w^2]_t` is the running average of squared parameter updates,
    - :math:`\rho` is the decay rate (typically 0.9),
    - :math:`\epsilon` is a small constant for numerical stability.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    rho: A coefficient used for computing a running average of squared
      gradients.
    eps: Term added to the denominator to improve numerical stability.
    weight_decay: Optional rate at which to decay weights.
    weight_decay_mask: A tree with same structure as (or a prefix of) the params
      PyTree, or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the transformation to, and `False` for those you want to skip.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> f = lambda x: jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.adadelta(learning_rate=10.)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.36E+01
    Objective function: 1.32E+01
    Objective function: 1.29E+01
    Objective function: 1.25E+01
    Objective function: 1.21E+01

  References:
    Zeiler, `Adadelta: An Adaptive Learning Rate Optimizer
    <https://arxiv.org/pdf/1212.5701.pdf>`_, 2012
  """  # noqa: E501
  return combine.chain(
      transform.add_decayed_weights(weight_decay, mask=weight_decay_mask),
      transform.scale_by_adadelta(rho=rho, eps=eps),
      transform.scale_by_learning_rate(learning_rate),
  )

