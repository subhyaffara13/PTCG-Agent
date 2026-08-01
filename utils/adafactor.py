
def adafactor(
    params: list[Tensor],
    grads: list[Tensor],
    row_vars: list[Tensor | None],
    col_vars: list[Tensor | None],
    variances: list[Tensor | None],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    foreach: bool | None = None,
    grad_scale: Tensor | None = None,
    found_inf: Tensor | None = None,
    has_complex: bool = False,
    *,
    d: float,
    lr: float | Tensor,
    beta2_decay: float,
    weight_decay: float,
    eps1: float,
    eps2: float,
    maximize: bool,
) -> None:
    r"""Functional API that performs Adafactor algorithm computation.

    See :class:`~torch.optim.Adafactor` for details.
    """
    if not torch.compiler.is_compiling() and not all(
        isinstance(t, torch.Tensor) for t in state_steps
    ):
        raise RuntimeError(
            "`state_steps` argument must contain a list of singleton tensors"
        )

    if foreach:
        func = _multi_tensor_adafactor
    else:
        func = _single_tensor_adafactor

    func(
        params,
        grads,
        row_vars,
        col_vars,
        variances,
        state_steps,
        d=d,
        lr=lr,
        beta2_decay=beta2_decay,
        weight_decay=weight_decay,
        eps1=eps1,
        eps2=eps2,
        maximize=maximize,
        grad_scale=grad_scale,
        found_inf=found_inf,
        has_complex=has_complex,
    )


def adafactor(
    learning_rate: Optional[base.ScalarOrSchedule] = None,
    min_dim_size_to_factor: int = 128,
    decay_rate: jax.typing.ArrayLike = 0.8,
    decay_offset: jax.typing.ArrayLike = 0,
    multiply_by_parameter_scale: bool = True,
    clipping_threshold: Optional[jax.typing.ArrayLike] = 1.0,
    momentum: Optional[jax.typing.ArrayLike] = None,  # float
    dtype_momentum: jax.typing.DTypeLike = jnp.float32,
    weight_decay_rate: Optional[base.ScalarOrSchedule] = None,
    eps: jax.typing.ArrayLike = 1e-30,
    factored: bool = True,
    weight_decay_mask: MaskOrFn = None,
) -> base.GradientTransformationExtraArgs:
  """The Adafactor optimizer.

  Adafactor is an adaptive learning rate optimizer that focuses on fast
  training of large scale neural networks. It saves memory by using a factored
  estimate of the second order moments used to scale gradients.

  Args:
      learning_rate: A global scaling factor, either fixed or evolving along
        iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
        Note that the natural scale for Adafactor's LR is markedly different
        from Adam, one doesn't use the 1/sqrt(hidden) correction for this optim
        with attention-based models.
      min_dim_size_to_factor: Only factor the statistics if two array dimensions
        have at least this size.
      decay_rate: Controls second-moment exponential decay schedule.
      decay_offset: For fine-tuning, one may set this to the starting step
        number of the fine-tuning phase.
      multiply_by_parameter_scale: If True, then scale learning_rate by
        parameter norm. If False, provided learning_rate is absolute step size.
      clipping_threshold: Optional clipping threshold. Must be >= 1. If None,
        clipping is disabled.
      momentum: Optional value between 0 and 1, enables momentum and uses extra
        memory if non-None! None by default.
      dtype_momentum: Data type of momentum buffers.
      weight_decay_rate: Optional rate at which to decay weights.
      eps: Regularization constant for root mean squared gradient.
      factored: Whether to use factored second-moment estimates.
      weight_decay_mask: A tree with same structure as (or a prefix of) the
        params PyTree, or a Callable that returns such a pytree given the
        params/updates. The leaves should be booleans, `True` for
        leaves/subtrees you want to apply the transformation to, and `False` for
        those you want to skip.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.adafactor(learning_rate=0.003)
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
    Objective function: 1.38E+01
    Objective function: 1.37E+01
    Objective function: 1.36E+01

  References:
    Shazeer et al, `Adafactor: Adaptive Learning Rates with Sublinear Memory
    Cost <https://arxiv.org/abs/1804.04235>`_, 2018
  """
  # The core of the algorithm is a procedure for rescaling gradients
  # by a factored estimate of the root mean squared gradients.
  # This reduces memory compared to algorithms such as Adam or RmsProp,
  # by not having to hold a separate estimate for each weight.
  tx = [
      factorized.scale_by_factored_rms(
          factored, decay_rate, decay_offset, min_dim_size_to_factor, eps
      )
  ]
  # This basic rescaling is typically combined with one or more of the following
  # transformation (all can be disabled via adafactor's constructor args).
  if clipping_threshold is not None:
    tx.append(_clipping.clip_by_block_rms(clipping_threshold))
  if learning_rate is not None:
    tx.append(transform.scale_by_learning_rate(learning_rate, flip_sign=False))
  if multiply_by_parameter_scale:
    tx.append(transform.scale_by_param_block_rms())
  if momentum is not None:
    tx.append(
        transform.ema(momentum, debias=False, accumulator_dtype=dtype_momentum)
    )
  if weight_decay_rate is not None:
    tx.append(
        transform.add_decayed_weights(weight_decay_rate, mask=weight_decay_mask)
    )
  # In gradient "descent" we follow the negative gradient.
  tx.append(transform.scale(-1))
  return combine.chain(*tx)

