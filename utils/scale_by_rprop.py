
def scale_by_rprop(
    learning_rate: jax.typing.ArrayLike,
    eta_minus: jax.typing.ArrayLike = 0.5,
    eta_plus: jax.typing.ArrayLike = 1.2,
    min_step_size: jax.typing.ArrayLike = 1e-6,
    max_step_size: jax.typing.ArrayLike = 50.0,
) -> base.GradientTransformation:
  """Scale with the Rprop optimizer.

  See :func:`optax.rprop` for more details.

  Args:
    learning_rate: The initial step size.
    eta_minus: Multiplicative factor for decreasing step size. This is applied
      when the gradient changes sign from one step to the next.
    eta_plus: Multiplicative factor for increasing step size. This is applied
      when the gradient has the same sign from one step to the next.
    min_step_size: Minimum allowed step size. Smaller steps will be clipped to
      this value.
    max_step_size: Maximum allowed step size. Larger steps will be clipped to
      this value.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.
  """

  def init_fn(params):
    step_sizes = optax.tree.full_like(params, learning_rate)
    prev_updates = optax.tree.zeros_like(params)
    return ScaleByRpropState(step_sizes, prev_updates)

  def update_fn(updates, state, params=None):
    del params
    sign = jax.tree.map(
        lambda g, prev_g: g * prev_g, updates, state.prev_updates
    )
    step_sizes = jax.tree.map(
        lambda s, step_size: jnp.where(
            s == 0,
            step_size,
            jnp.clip(
                step_size * jnp.where(s > 0, eta_plus, eta_minus),
                min=min_step_size,
                max=max_step_size,
            ),
        ),
        sign,
        state.step_sizes,
    )
    prev_updates = jax.tree.map(
        lambda s, g, step_size: jnp.where(
            s < 0, jnp.zeros_like(g), step_size * jnp.sign(g)
        ),
        sign,
        updates,
        step_sizes,
    )
    updates = jax.tree.map(
        lambda s, g, prev_g: jnp.where(s < 0, jnp.zeros_like(prev_g), prev_g),
        sign,
        prev_updates,
        state.prev_updates,
    )
    return updates, ScaleByRpropState(step_sizes, prev_updates)

  return base.GradientTransformation(init_fn, update_fn)

