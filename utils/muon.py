from typing import Any, Callable, Optional, Union

def muon(
    params: list[Tensor],
    grads: list[Tensor],
    muon_momentum_bufs: list[Tensor],
    *,
    foreach: bool | None = None,
    lr: float,
    weight_decay: float,
    momentum: float,
    nesterov: bool,
    ns_coefficients: tuple[float, float, float],
    ns_steps: int,
    eps: float,
    adjust_lr_fn: str | None,
    has_complex: bool,
) -> None:
    r"""Functional API that performs Muon algorithm computation.

    See :class:`~torch.optim.Muon` for details.
    """
    if foreach is not None and foreach:
        raise RuntimeError("Foreach is not supported for Muon yet")

    func = _single_tensor_muon

    func(
        params,
        grads,
        muon_momentum_bufs,
        lr=lr,
        weight_decay=weight_decay,
        momentum=momentum,
        nesterov=nesterov,
        ns_coefficients=ns_coefficients,
        ns_steps=ns_steps,
        eps=eps,
        adjust_lr_fn=adjust_lr_fn,
        has_complex=has_complex,
    )


def muon(
    learning_rate: base.ScalarOrSchedule,
    ns_coeffs: Union[
        tuple[jax.typing.ArrayLike, jax.typing.ArrayLike, jax.typing.ArrayLike],
        tuple[
            tuple[
                jax.typing.ArrayLike, jax.typing.ArrayLike, jax.typing.ArrayLike
            ],
            ...,
        ],
        str,
    ] = _DEFAULT_NS_COEFFS,
    ns_steps: jax.typing.ArrayLike = 5,
    beta: jax.typing.ArrayLike = 0.95,
    eps: jax.typing.ArrayLike = 1e-8,
    weight_decay: jax.typing.ArrayLike = 0.0,
    weight_decay_mask: Optional[
        Union[Any, Callable[[base.Params], Any]]
    ] = None,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
    *,
    nesterov: bool = True,
    adaptive: bool = False,
    preconditioning: Literal[
        'frobenius', 'spectral', 'aol', 'schatten'
    ] = 'frobenius',
    adam_b1: jax.typing.ArrayLike = 0.9,
    adam_b2: jax.typing.ArrayLike = 0.999,
    adam_eps_root: jax.typing.ArrayLike = 0.0,
    adam_weight_decay: jax.typing.ArrayLike = 0.0,
    adam_learning_rate: base.ScalarOrSchedule | None = None,
    muon_weight_dimension_numbers: WeightDimNumOrFn | None = None,
    consistent_rms: jax.typing.ArrayLike | None = None,
) -> base.GradientTransformation:
  r"""Muon: Momentum Orthogonalized by Newton-schulz.

  Muon is a variant of Shampoo that uses the Newton-schulz method to
  orthogonalize the momentum accumulated by the optimizer. Mathematically, it
  does steepest descent under the Schatten-p norm, for some large p. With
  p=infty, it is equivalent to Shampoo without accumulation, or steepest
  descent under the Spectral norm.

  Note that Muon is currently only defined for 2D parameters, i.e. matrices.
  This is because the Newton-Schulz iterator expects a matrix as input.
  The non-2D parameters are instead passed through an AdamW optimizer
  (using a weight decay of 0 as default).

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    ns_coeffs: Coefficients for the Newton-schulz method (can be a string
      indicator for a preset). Existing presets: `muon`, `dion`.
    ns_steps: Number of Newton-schulz iterations.
      Ignored if `ns_coeffs` is a tuple of tuples.
    beta: Decay rate for the exponentially weighted average of grads.
    eps: Term added to the denominator to improve numerical stability.
    weight_decay: Strength of the weight decay regularization. Note that this
      weight decay is multiplied with the learning rate. This is consistent
      with other frameworks such as PyTorch, but different from
      (Loshchilov et al, 2019) where the weight decay is only multiplied with
      the "schedule multiplier", but not the base learning rate.
    weight_decay_mask: A tree with same structure as (or a prefix of) the params
      PyTree, or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the weight decay to, and `False` for those you want to skip.
    mu_dtype: Data type of the momentum accumulator.
    nesterov: Whether to use Nesterov momentum.
    adaptive: Whether to scale the updates by the dual norm of the
      original updates. See <https://arxiv.org/abs/2409.20325>
    preconditioning: What type of preconditioning to use before NS iterations.
      Available options are:
      - 'frobenius' (default): Use Frobenius rescaling before NS:
        safe, standard, but degrades orthogonalization quality when using
        less than 5 NS steps.
      - 'spectral' : Use Spectral norm rescaling before NS:
        much more computationally intensive, but better orthogonalization
        quality.
      - 'aol': Use AOL rescalings to improve orthogonality with little to
        no overhead, usually allows the user to remove one iterative NS step.
        See <https://arxiv.org/abs/2512.04632>.
      - 'schatten': Use the Schatten-4 norm for rescaling,
        allows for better performance with little to no extra cost.
        See <https://arxiv.org/abs/2506.10935>.
    adam_b1: Exponential decay rate for Adam's first moment estimates.
    adam_b2: Exponential decay rate for Adam's second moment estimates.
    adam_eps_root: Epsilon to stabilize division in Adam, square root version.
    adam_weight_decay: Weight decay factor for Adam.
    adam_learning_rate: Auxiliary learning rate for the Adam optimizer.
      If `None`, the learning rate for Adam defaults to the same as Muon.
    muon_weight_dimension_numbers: An optional tree of `MuonDimensionNumbers`s,
      specifying how to reshape the parameters for orthogonalization otherwise
      muon parameters are assumed to be 2D matrices. A `None` value indicates
      that the parameter is not a muon parameter and will be optimized with
      Adam. A callable takes as input the params and returns a possibly masked
      pytree of specs, similar to `weight_decay_mask`. If not provided, muon is
      applied to all 2D parameters.
    consistent_rms: An optional float to activate consistent RMS scaling.
      Scales updates by `sqrt(max(fan_in, fan_out)) * consistent_rms` to make
      root mean square (RMS) shape-independent, like AdamW. `0.2` is recommended
      to match AdamW's empirical RMS. See <https://arxiv.org/abs/2502.16982>.
      If `None`, uses width scaling `sqrt(max(1, fan_out / fan_in))`.

  Returns:
    The corresponding `GradientTransformation`.

  References:
    Jordan, `modded-nanogpt: Speedrunning the NanoGPT baseline
    <https://github.com/KellerJordan/modded-nanogpt>`_, 2024

    Bernstein et al., `Old Optimizer, New Norm: An Anthology
    <https://arxiv.org/abs/2409.20325>`_, 2024

    Liu et al., `Muon is Scalable for LLM Training`,
    <https://arxiv.org/abs/2502.16982>`_, 2025

    Boissin et al., `Turbo-Muon: Accelerating Orthogonality-Based
    Optimization with Pre-Conditioning`,
    <https://arxiv.org/abs/2512.04632>`_, 2025

    Ahn et al., `Dion: Distributed Orthonormalized Updates`,
    <https://arxiv.org/abs/2504.05295>`_, 2025

    Grishina et al., `Accelerating Newton-Schulz Iteration for Orthogonalization
    via Chebyshev-type Polynomials`,
    <https://arxiv.org/abs/2506.10935>`_, 2025

    Amsel et al., `The Polar Express: Optimal Matrix Sign Methods and Their
    Application to the Muon Algorithm`,
    <https://arxiv.org/pdf/2505.16932>`, 2025
  """

  if adam_learning_rate is None:
    adam_learning_rate = learning_rate

  if isinstance(ns_coeffs, str):
    if ns_coeffs not in _NS_COEFFS_PRESET_DICT:
      raise ValueError(f'Unknown ns_coeff preset string: {ns_coeffs}')
    ns_coeffs_ = _NS_COEFFS_PRESET_DICT[ns_coeffs]
  else:
    ns_coeffs_ = ns_coeffs

  # None at root indicates the default 2D rule.
  if muon_weight_dimension_numbers is None:
    param_labels = lambda params: jax.tree.map(
        lambda x: 'muon' if x.ndim == 2 else 'adam', params
    )
    muon_weight_dimension_numbers = MuonDimensionNumbers()
  else:
    def param_labels(params):
      dim_nums = (muon_weight_dimension_numbers(params)
                  if callable(muon_weight_dimension_numbers)
                  else muon_weight_dimension_numbers)
      populate_subtree_ = lambda dim_num, x: jax.tree.map(
          lambda y: 'muon' if dim_num is not None else 'adam', x)
      # Dimension numbers come first since they can be a prefix mask.
      return jax.tree.map(populate_subtree_, dim_nums, params,
                          is_leaf=lambda x: x is None or _is_weight_dim_nums(x))

  # We need to normalize the dimension numbers because they have to match the
  # tree structure of the masked muon state tree (see `combine.partition`).
  def muon_weight_dim_nums_fn(params):
    # if muon_weight_dimension_numbers is None:
    #   return None
    # Normalize the dimension numbers for `combine.partition`.
    # Insert MaskedNode() where muon state will be masked out.
    dim_nums = (muon_weight_dimension_numbers(params)
                if callable(muon_weight_dimension_numbers)
                else muon_weight_dimension_numbers)
    mask = jax.tree.map(lambda label: label == 'muon', param_labels(params))
    is_leaf = lambda x: (x is None or _is_weight_dim_nums(x)
                         or isinstance(x, _masking.MaskedNode))
    populate_subtree_ = lambda dim_nums, submask: jax.tree.map(
        lambda m: dim_nums if m else _masking.MaskedNode(), submask)
    return jax.tree.map(populate_subtree_, dim_nums, mask, is_leaf=is_leaf)

  return combine.partition(
      transforms={
          'muon': combine.chain(
              scale_by_muon(
                  ns_coeffs=ns_coeffs_,
                  ns_steps=ns_steps,
                  beta=beta,
                  eps=eps,
                  mu_dtype=mu_dtype,
                  nesterov=nesterov,
                  adaptive=adaptive,
                  preconditioning=preconditioning,
                  weight_dimension_numbers=muon_weight_dim_nums_fn,
              ),
              scale_by_shape(
                  weight_dimension_numbers=muon_weight_dim_nums_fn,
                  consistent_rms=consistent_rms,
              ),
              transform.add_decayed_weights(weight_decay, weight_decay_mask),
              transform.scale_by_learning_rate(learning_rate),
          ),
          'adam': alias.adamw(
              learning_rate=adam_learning_rate,
              b1=adam_b1,
              b2=adam_b2,
              eps=eps,
              eps_root=adam_eps_root,
              weight_decay=adam_weight_decay,
              mu_dtype=mu_dtype,
              nesterov=nesterov,
          ),
      },
      param_labels=param_labels,
  )

