
def scale_by_muon(
    ns_coeffs: Union[
        tuple[jax.typing.ArrayLike, jax.typing.ArrayLike, jax.typing.ArrayLike],
        tuple[
            tuple[
                jax.typing.ArrayLike, jax.typing.ArrayLike, jax.typing.ArrayLike
            ],
            ...,
        ],
    ] = _DEFAULT_NS_COEFFS,
    ns_steps: jax.typing.ArrayLike = 5,
    beta: jax.typing.ArrayLike = 0.95,
    eps: jax.typing.ArrayLike = 1e-8,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
    *,
    nesterov: bool = True,
    adaptive: bool = False,
    preconditioning: Literal[
        'frobenius', 'spectral', 'aol', 'schatten'
    ] = 'frobenius',
    weight_dimension_numbers: WeightDimNumOrFn | None = None,
) -> base.GradientTransformation:
  r"""Rescale updates according to the Muon algorithm.

  Muon is a variant of Shampoo that uses the Newton-schulz method to
  orthogonalize the momentum accumulated by the optimizer. Mathematically, it
  does steepest descent under the Schatten-p norm, for some large p. With
  p=infty, it is equivalent to Shampoo without accumulation, or steepest
  descent under the Spectral norm.

  Args:
    ns_coeffs: Coefficients for the Newton-schulz method.
    ns_steps: Number of Newton-schulz iterations.
      Ignored if `ns_coeffs` is a tuple of tuples.
    beta: Decay rate for the exponentially weighted average of grads.
    eps: Term added to denominators to improve numerical stability.
    mu_dtype: Data type of the momentum accumulator.
    nesterov: Whether to use Nesterov momentum.
    adaptive: Whether to scale the updates by the dual norm of the
      original updates. See <https://arxiv.org/abs/2409.20325>
    preconditioning: What type of preconditioning to use before NS iterations.
      Available options are:
      - 'frobenius' (default): Use Frobenius rescaling before NS.
      - 'spectral' : Use Spectral norm rescaling before NS.
      - 'aol': Use AOL rescaling to improve orthogonality.
      - 'schatten': Use the Schatten-4 norm for rescaling.
    weight_dimension_numbers: An optional tree with the same structure as the
      params of `MuonDimensionNumbers`s, specifying how to reshape the
      parameters before and after the orthogonalization OR a callable returning
      such a tree. None implies that all parameters are 2D matrices.

  Returns:
    A `GradientTransformation` object.

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
  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params):
    mu = optax.tree.zeros_like(params, dtype=mu_dtype)  # First moment
    ns_coeffs_ = jnp.asarray(ns_coeffs)

    if ns_coeffs_.ndim > 2 or ns_coeffs_.shape[-1] != 3:
      raise ValueError(
          f'ns_coeffs must have shape (3,) or (n, 3), got {ns_coeffs_.shape}'
      )
    if ns_coeffs_.ndim == 2:
      if not ns_coeffs_.shape[0] <= ns_steps:
        raise ValueError(f'Not enough coeffs to perform {ns_steps} steps')
      ns_coeffs_ = ns_coeffs_[-ns_steps:]

    return MuonState(
        count=jnp.zeros([], jnp.int32),
        mu=mu,
        ns_coeffs=ns_coeffs_,
    )

  def update_fn(updates, state, params=None):
    del params
    # TODO(rdyro): extend to _masking._mask_callable
    if callable(weight_dimension_numbers):
      # Populate weight_dim_nums if it's a callable. Use updates instead of
      # actual params since only shapes matter and params may not be provided.
      resolved_weight_dim_nums = weight_dimension_numbers(updates)
    else:
      resolved_weight_dim_nums = weight_dimension_numbers

    mu = optax.tree.update_moment(updates, state.mu, beta, 1)
    count_inc = numerics.safe_increment(state.count)
    if nesterov:
      mu_hat = jax.tree.map(
          lambda m, g: beta * m + (1 - beta) * g,
          optax.tree.bias_correction(
              mu, beta, numerics.safe_increment(count_inc)
          ),
          optax.tree.bias_correction(updates, beta, count_inc),
      )
    else:
      mu_hat = optax.tree.bias_correction(mu, beta, count_inc)
    # Apply Newton-schulz orthogonalization.
    updates = jax.tree.map(
        lambda x, dim_num: orthogonalize_via_newton_schulz(
            x, state.ns_coeffs, ns_steps, preconditioning, eps, dim_num),
        mu_hat, resolved_weight_dim_nums, is_leaf=_is_weight_dim_nums)
    if adaptive:
      # Scale the orthogonalized updates by the dual norm of the original
      # updates. See https://arxiv.org/abs/2409.20325 for the derivation.
      updates = jax.tree.map(
          lambda x, y: jnp.sum(x.conj() * y) * y, mu_hat, updates
      )

    mu = optax.tree.cast(mu, mu_dtype)
    return updates, MuonState(
        count=count_inc,
        mu=mu,
        ns_coeffs=state.ns_coeffs,
    )
  return base.GradientTransformation(init_fn, update_fn)

