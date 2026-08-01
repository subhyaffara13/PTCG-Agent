
def sample_agent_position(
    key: chex.PRNGKey, circle_radius: float, center_init: bool
) -> chex.Array:
    """Sample a random position in circle (or set position to center)."""
    rng_radius, rng_angle = jax.random.split(key)
    sampled_radius = jax.random.uniform(rng_radius, minval=0, maxval=circle_radius)
    sampled_angle = jax.random.uniform(rng_angle, minval=0, maxval=jnp.pi)

    pos = jax.lax.select(
        center_init,
        jnp.zeros(2),
        jnp.array(
            [
                sampled_radius * jnp.cos(sampled_angle),
                sampled_radius * jnp.sin(sampled_angle),
            ]
        ),
    )
    return pos

