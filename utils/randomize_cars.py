
def randomize_cars(
    speeds: chex.Array,
    directions: chex.Array,
    old_cars: chex.Array,
    initialize: bool,
) -> chex.Array:
    """Randomize car speeds & directions. Reset position if initialize."""
    speeds_new = directions * speeds
    new_cars = jnp.zeros((8, 4), dtype=int)

    # Loop over all 8 cars and set their data
    for i in range(8):
        # Reset both speeds, directions and positions
        new_cars = new_cars.at[i, :].set(
            [0, i + 1, jnp.abs(speeds_new[i]), speeds_new[i]],
        )
        # Reset only speeds and directions
        old_cars = old_cars.at[i, 2:4].set(
            [jnp.abs(speeds_new[i]), speeds_new[i]],
        )

    # Mask the car array manipulation according to initialize
    cars = jax.lax.select(initialize, new_cars, old_cars)
    return jnp.array(cars, dtype=jnp.int_)

