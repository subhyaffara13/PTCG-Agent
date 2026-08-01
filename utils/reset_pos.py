
def reset_pos(rng: chex.PRNGKey, coords: chex.Array) -> chex.Array:
    """Reset the position of the agent."""
    pos_index = jax.random.randint(rng, (), 0, coords.shape[0])
    return coords[pos_index][:]


def reset_pos(rng: chex.PRNGKey, coords: chex.Array, goal: chex.Array) -> chex.Array:
    """Reset the position of the agent."""
    pos_index = jax.random.randint(rng, (), 0, coords.shape[0] - 1)
    collision = jnp.logical_and(
        coords[pos_index][0] == goal[0], coords[pos_index][1] == goal[1]
    )
    pos_index = jax.lax.select(collision, coords.shape[0] - 1, pos_index)
    return coords[pos_index][:]

