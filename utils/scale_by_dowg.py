
def scale_by_dowg(
    init_estim_sq_dist: Optional[jax.typing.ArrayLike] = None,
    eps: jax.typing.ArrayLike = 1e-4,
) -> base.GradientTransformation:
  """Scale by Distance over Weighted Gradients (DoWG).

  See :func:`optax.contrib.dowg` for more details.

  Args:
    init_estim_sq_dist: initial guess of the squared distance to solution.
    eps: small value to prevent division by zero in the denominator defining,
      the learning rate, also used as initial guess for the distance to solution
      if ``init_estim_sq_dist`` is None.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  .. versionadded:: 0.2.3
  """

  def init_fn(params: base.Params) -> DoWGState:
    # Define state parameters with the lowest dtype of the parameters to avoid
    # dtype promotion of parameters resulting in a dtype mismatch between
    # parameters and updates.
    params_dtype = optax.tree.dtype(params, "lowest")
    if init_estim_sq_dist is None:
      init_estim_sq_dist_ = eps
    else:
      init_estim_sq_dist_ = init_estim_sq_dist
    return DoWGState(
        init_params=params,
        estim_sq_dist=jnp.asarray(init_estim_sq_dist_, dtype=params_dtype),
        weighted_sq_norm_grads=jnp.asarray(0.0, dtype=params_dtype),
    )

  def update_fn(
      updates: base.Updates, state: DoWGState, params: base.Params
  ) -> tuple[base.Updates, DoWGState]:
    curr_sq_dist = optax.tree.norm(
        optax.tree.sub(state.init_params, params), squared=True
    )
    estim_sq_dist = jnp.maximum(state.estim_sq_dist, curr_sq_dist)
    step_sq_norm_grads = optax.tree.norm(updates, squared=True)
    weighted_sq_norm_grads = (
        estim_sq_dist * step_sq_norm_grads + state.weighted_sq_norm_grads
    )
    learning_rate = estim_sq_dist / (jnp.sqrt(weighted_sq_norm_grads) + eps)

    new_updates = optax.tree.scale(learning_rate, updates)
    return new_updates, state._replace(
        estim_sq_dist=estim_sq_dist,
        weighted_sq_norm_grads=weighted_sq_norm_grads,
    )

  return base.GradientTransformation(init_fn, update_fn)

