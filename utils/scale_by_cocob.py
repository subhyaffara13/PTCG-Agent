
def scale_by_cocob(
    alpha: jax.typing.ArrayLike = 100.0, eps: jax.typing.ArrayLike = 1e-8
) -> base.GradientTransformation:
  """Rescale updates according to the COntinuous COin Betting algorithm.

  See :func:`optax.contrib.cocob` for more details.

  Args:
    alpha: fraction to bet parameter of the COCOB optimizer
    eps: jitter term to avoid dividing by 0

  Returns:
    A `GradientTransformation` object.
  """

  def init_fn(params):
    init_adapt = optax.tree.zeros_like(params)
    init_scale = optax.tree.ones_like(params)
    init_scale = optax.tree.scale(eps, init_scale)
    return COCOBState(
        init_particles=params,
        cumulative_gradients=init_adapt,
        scale=init_scale,
        subgradients=init_adapt,
        reward=init_adapt,
    )

  def update_fn(updates, state, params):
    init_particles, cumulative_grads, scale, subgradients, reward = state

    scale = jax.tree.map(
        lambda L, c: jnp.maximum(L, jnp.abs(c)), scale, updates
    )
    subgradients = jax.tree.map(
        lambda G, c: G + jnp.abs(c), subgradients, updates
    )
    reward = jax.tree.map(
        lambda R, c, p, p0: jnp.maximum(R - c * (p - p0), 0),
        reward,
        updates,
        params,
        init_particles,
    )
    cumulative_grads = jax.tree.map(
        lambda C, c: C - c, cumulative_grads, updates
    )

    new_updates = jax.tree.map(
        lambda p, p0, C, L, G, R: (
            -p + (p0 + C / (L * jnp.maximum(G + L, alpha * L)) * (L + R))
        ),
        params,
        init_particles,
        cumulative_grads,
        scale,
        subgradients,
        reward,
    )

    new_state = COCOBState(
        init_particles=init_particles,
        cumulative_gradients=cumulative_grads,
        scale=scale,
        subgradients=subgradients,
        reward=reward,
    )
    return new_updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

