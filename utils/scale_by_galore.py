
def scale_by_galore(
    rank: int = 128,
    update_proj_gap: int = 200,
    scale: float = 1.0,
    base_optimizer: Optional[base.GradientTransformation] = None,
    weight_dimension_numbers: Optional[GaLoreDimNumsOrFn] = None,
) -> base.GradientTransformation:
  """Scale updates using GaLore (Gradient Low-Rank Projection).

  GaLore projects gradients of 2D weight matrices into a low-rank subspace,
  significantly reducing memory for optimizer states while maintaining
  full-parameter learning.

  For tensors that are logically 2D but stored with higher dimensions (e.g.,
  attention projections as [embedding, heads, head_dim]), use
  ``weight_dimension_numbers`` to specify which axes form the matrix.

  .. warning::
    The ``base_optimizer`` must be a **gradient scaling transformation** that
    does NOT require parameter values (e.g.,``scale_by_adam``, ``scale_by_sgd``,
    ``scale_by_lion``). Optimizers that require ``params`` in their update
    function will fail because the base optimizer operates on low-rank shaped
    tensors, not the original parameter shapes.

    **Incompatible optimizers** (will crash or produce incorrect results):

    - ``adamw``, ``lamb``, ``lars``: require params for weight decay or
      trust ratio computation
    - Any optimizer using ``add_decayed_weights`` internally

    **Compatible optimizers**:

    - ``scale_by_adam``, ``scale_by_amsgrad``, ``scale_by_lion``
    - ``scale_by_rms``, ``scale_by_stddev``, ``scale_by_rss``
    - ``sgd`` (with learning_rate=1.0), ``scale_by_schedule``

    For weight decay, use the ``galore`` wrapper with its ``weight_decay``
    parameter, which correctly applies decoupled weight decay in the full
    parameter space.

  Args:
    rank: Target rank for the low-rank projection. Lower rank = less memory
      but potentially slower convergence.
    update_proj_gap: Number of steps between projection matrix updates.
      The projection matrices are recomputed from gradient SVD every this
      many steps.
    scale: Scaling factor applied to the final updates.
    base_optimizer: The base gradient transformation to apply in the low-rank
      subspace for 2D params and full space for non-2D params. Must be a
      gradient-only transformation (see warning above). If None, defaults to
      ``transform.scale_by_adam()``.
    weight_dimension_numbers: Specifies how to treat non-2D tensors as 2D
      matrices. Can be:

      - None: Only project naturally 2D parameters (default behavior)
      - A single ``GaLoreDimensionNumbers``: Apply to all parameters
      - A pytree matching params structure with ``GaLoreDimensionNumbers`` at
        leaves (use None for params to skip)
      - A callable taking params and returning such a pytree

  Returns:
    A GradientTransformation implementing GaLore.

  References:
    Zhao et al., `GaLore: Memory-Efficient LLM Training by Gradient Low-Rank
    Projection <https://arxiv.org/abs/2403.03507>`_, 2024
  """
  if base_optimizer is None:
    base_optimizer = transform.scale_by_adam()

  if not isinstance(rank, int):
    raise TypeError(f"`rank` must be an int, got {type(rank)}")
  if rank <= 0:
    raise ValueError(f"`rank` must be positive, got {rank}")

  def _get_dim_nums(params):
    """Resolve dimension numbers for each parameter."""
    if weight_dimension_numbers is None:
      # Default: only 2D params get projected, with standard axes
      return jax.tree.map(
          lambda p: GaLoreDimensionNumbers() if p.ndim == 2 else None, params
      )
    elif callable(weight_dimension_numbers):
      return weight_dimension_numbers(params)
    elif _is_galore_dim_nums(weight_dimension_numbers):
      # Single spec applied to all applicable params
      return jax.tree.map(
          lambda p: weight_dimension_numbers if p.ndim >= 2 else None, params
      )
    else:
      # Already a pytree of dimension numbers
      return weight_dimension_numbers

  def _compute_projection_shapes(p, dim_num):
    """Compute projector and proxy shapes for a parameter."""
    if dim_num is None:
      # No projection for this parameter
      return jnp.zeros((0, 0), dtype=p.dtype), jnp.zeros_like(p)

    # Reshape to 2D for shape computation
    reshape_fn, _ = _compute_galore_reshape(p, dim_num)
    p_2d = reshape_fn(p)
    m_dim, n_dim = p_2d.shape

    use_left = m_dim >= n_dim
    effective_rank = min(rank, m_dim, n_dim)

    if use_left:
      projector_shape = (m_dim, effective_rank)
      proxy_shape = (effective_rank, n_dim)
    else:
      projector_shape = (n_dim, effective_rank)
      proxy_shape = (m_dim, effective_rank)

    projector = jnp.zeros(projector_shape, dtype=p.dtype)
    proxy = jnp.zeros(proxy_shape, dtype=p.dtype)
    return projector, proxy

  def init_fn(params: base.Params) -> GaLoreState:
    # Handle empty trees (e.g., _ParamsPlaceholder from tree_map_params)
    param_leaves, _ = jax.tree.flatten(params)
    if not param_leaves:
      # Empty params - return matching empty state
      base_state = base_optimizer.init(params)
      return GaLoreState(
          count=jnp.zeros([], jnp.int32),
          base_optimizer_state=base_state,
          projector=params,  # Same empty structure
      )

    dim_nums = _get_dim_nums(params)

    # Compute projector and proxy shapes for each parameter
    results = jax.tree.map(
        _compute_projection_shapes,
        params,
        dim_nums,
        is_leaf=_is_dim_nums_leaf,
    )
    projectors, proxies = jax.tree.transpose(
        jax.tree.structure(params),
        jax.tree.structure((0, 0)),
        results,
    )

    # Initialize base optimizer with proxy params (low-rank shaped)
    base_state = base_optimizer.init(proxies)

    return GaLoreState(
        count=jnp.zeros([], jnp.int32),
        base_optimizer_state=base_state,
        projector=projectors,
    )

  def update_fn(
      updates: base.Updates,
      state: GaLoreState,
      params: Optional[base.Params] = None,
  ) -> tuple[base.Updates, GaLoreState]:
    """Apply GaLore update."""
    del params
    count = state.count
    count_inc = numerics.safe_int32_increment(count)
    should_update_proj = (count % update_proj_gap) == 0

    dim_nums = _get_dim_nums(updates)

    def project_to_low_rank(grad, projector, dim_num):
      """Project gradient to low-rank subspace and update projector."""
      if dim_num is None:
        # No projection for this parameter
        return grad, projector

      original_dtype = grad.dtype

      # Reshape to 2D
      reshape_fn, _ = _compute_galore_reshape(grad, dim_num)
      grad_2d = reshape_fn(grad)
      m_dim, n_dim = grad_2d.shape

      effective_rank = min(rank, m_dim, n_dim)
      use_left = m_dim >= n_dim

      if use_left:
        def compute_left_projector():
          grad_f32 = grad_2d.astype(jnp.float32)
          u, _, _ = jnp.linalg.svd(grad_f32, full_matrices=False)
          return u[:, :effective_rank].astype(original_dtype)

        new_projector = jax.lax.cond(
            should_update_proj,
            compute_left_projector,
            lambda: projector,
        )
        low_rank_grad = new_projector.T @ grad_2d
      else:
        def compute_right_projector():
          grad_f32 = grad_2d.astype(jnp.float32)
          _, _, vh = jnp.linalg.svd(grad_f32, full_matrices=False)
          return vh[:effective_rank, :].T.astype(original_dtype)

        new_projector = jax.lax.cond(
            should_update_proj,
            compute_right_projector,
            lambda: projector,
        )
        low_rank_grad = grad_2d @ new_projector

      return low_rank_grad, new_projector

    def project_back_to_full(
        low_rank_update, projector, original_grad, dim_num
    ):
      """Project low-rank update back to full space."""
      if dim_num is None:
        return low_rank_update

      original_dtype = original_grad.dtype

      # Get inverse reshape function
      _, inverse_fn = _compute_galore_reshape(original_grad, dim_num)
      reshape_fn, _ = _compute_galore_reshape(original_grad, dim_num)
      grad_2d = reshape_fn(original_grad)
      m_dim, n_dim = grad_2d.shape
      use_left = m_dim >= n_dim

      if use_left:
        upd_2d = projector @ low_rank_update
      else:
        upd_2d = low_rank_update @ projector.T

      # Reshape back to original shape
      upd = inverse_fn(upd_2d)
      return (scale * upd).astype(original_dtype)

    # Step 1: Project all gradients to low-rank subspace
    projected_results = jax.tree.map(
        project_to_low_rank,
        updates,
        state.projector,
        dim_nums,
        is_leaf=_is_dim_nums_leaf,
    )
    low_rank_grads, new_projectors = jax.tree.transpose(
        jax.tree.structure(updates),
        jax.tree.structure((0, 0)),
        projected_results,
    )

    # Step 2: Apply base optimizer in low-rank space
    low_rank_updates, new_base_state = base_optimizer.update(
        low_rank_grads, state.base_optimizer_state, None
    )

    # Step 3: Project updates back to full space
    full_updates = jax.tree.map(
        project_back_to_full,
        low_rank_updates,
        new_projectors,
        updates,
        dim_nums,
        is_leaf=_is_dim_nums_leaf,
    )

    new_state = GaLoreState(
        count=count_inc,
        base_optimizer_state=new_base_state,
        projector=new_projectors,
    )

    return full_updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

