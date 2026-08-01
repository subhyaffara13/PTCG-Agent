
def scale_by_dog(
    init_step: tuple[Literal["distance", "learning_rate", "heuristic"],
                     jax.typing.ArrayLike],
    eps: jax.typing.ArrayLike = 1e-8,
) -> base.GradientTransformation:
  r"""Scale by Distance over Gradients (DoG).

  See :func:`optax.contrib.dog` for more details.

  Args:
    init_step: Initial step specification.
    eps: Epsilon used for numerical stability.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  .. versionadded:: 0.2.3

  .. warning::
    The authors recommend using model averaging with this optimizer.

    This optimizer's ``init`` function should receive the actual parameters (not
    just dummy parameters) when the ``heuristic`` initial step is used.
  """

  init_step_type, init_step_value = init_step

  def init_fn(params: base.Params) -> DoGState:
    # Define state parameters with the lowest dtype of the parameters to avoid
    # dtype promotion of parameters resulting in a dtype mismatch between
    # parameters and updates.
    params_dtype = optax.tree.dtype(params, "lowest")

    if init_step_type == "distance":
      r_epsilon = init_step_value
    elif init_step_type == "heuristic":
      r_epsilon = init_step_value * (1 + optax.tree.norm(params))
    elif init_step_type == "learning_rate":
      r_epsilon = 0.0
    else:
      raise ValueError(
          f"Invalid init_step specification for scale_by_dog: {init_step_type=}"
      )

    return DoGState(
        is_init_step=jnp.asarray(True),
        init_params=params,
        max_dist=jnp.asarray(r_epsilon, dtype=params_dtype),
        sum_sq_norm_grads=jnp.asarray(0.0, dtype=params_dtype),
    )

  def update_fn(
      updates: base.Updates, state: DoGState, params: base.Params
  ) -> tuple[base.Updates, DoGState]:
    dist = optax.tree.norm(optax.tree.sub(state.init_params, params))
    max_dist = jnp.maximum(state.max_dist, dist)
    sum_sq_norm_grads = state.sum_sq_norm_grads + optax.tree.norm(
        updates, squared=True
    )
    learning_rate = max_dist / jnp.sqrt(sum_sq_norm_grads + eps)

    if init_step_type == "learning_rate":
      learning_rate = jnp.where(
          state.is_init_step, init_step_value, learning_rate
      )

    new_updates = optax.tree.scale(learning_rate, updates)
    return new_updates, DoGState(
        is_init_step=jnp.asarray(False),
        init_params=state.init_params,
        max_dist=max_dist,
        sum_sq_norm_grads=sum_sq_norm_grads,
    )

  return base.GradientTransformation(init_fn, update_fn)

