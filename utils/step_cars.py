
def step_cars(state: EnvState) -> EnvState:
    """Perform 3rd part of step transition for car."""
    # Update cars and check for collisions! - respawn agent at bottom
    pos = state.pos
    cars = state.cars
    for car_id in range(8):
        # Check for agent collision with car and if so reset agent
        collision_cond = jnp.logical_and(
            cars[car_id][0] == 4,
            cars[car_id][1] == pos,
        )

        pos = jax.lax.select(collision_cond, 9, pos)

        # Check for exiting frame, reset car and then check collision again
        car_cond = cars[car_id][2] == 0
        upd_2 = jax.lax.select(car_cond, jnp.abs(cars[car_id][3]), cars[car_id][2])

        cars = cars.at[car_id, 2].set(upd_2)
        upd_0 = jax.lax.select(
            car_cond,
            (
                cars[car_id][0]
                + 1 * (cars[car_id][3] > 0)
                - 1 * (1 - (cars[car_id][3] > 0))
            ),
            cars[car_id][0],
        )
        cars = cars.at[car_id, 0].set(upd_0)

        cond_sm_0 = jnp.logical_and(car_cond, cars[car_id][0] < 0)
        upd_0_sm = jax.lax.select(cond_sm_0, 9, cars[car_id][0])
        cars = cars.at[car_id, 0].set(upd_0_sm)
        cond_gr_9 = jnp.logical_and(car_cond, cars[car_id][0] > 9)
        upd_0_gr = jax.lax.select(cond_gr_9, 0, cars[car_id][0])
        cars = cars.at[car_id, 0].set(upd_0_gr)

        # Check collision after car position update - respawn agent
        # Note: Need to reevaluate collision condition since cars change!
        collision_cond = jnp.logical_and(
            cars[car_id][0] == 4,
            cars[car_id][1] == pos,
        )
        cond_pos = jnp.logical_and(car_cond, collision_cond)
        pos = jax.lax.select(cond_pos, 9, pos)
        # Move car if no previous car_cond update
        alt_upd_2 = jax.lax.select(car_cond, cars[car_id][2], cars[car_id][2] - 1)
        cars = cars.at[car_id, 2].set(alt_upd_2)
    # 4. Update various timers
    move_timer = state.move_timer - (state.move_timer > 0)
    return state.replace(pos=pos, cars=cars, move_timer=move_timer)

