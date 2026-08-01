
def step_timers(state: EnvState, params: EnvParams) -> EnvState:
    """Update various timers and check the ramping condition."""
    spawn_timer = state.spawn_timer - 1
    move_timer = state.move_timer - 1

    # Ramp difficulty if interval has elapsed
    ramp_cond = jnp.logical_and(
        params.ramping,
        jnp.logical_or(state.spawn_speed > 1, state.move_speed > 1),
    )
    # 1. Update ramp_timer
    timer_cond = jnp.logical_and(ramp_cond, state.ramp_timer >= 0)
    ramp_timer = jax.lax.select(timer_cond, state.ramp_timer - 1, params.ramp_interval)
    # 2. Update move_speed
    move_speed_cond = jnp.logical_and(
        jnp.logical_and(ramp_cond, 1 - timer_cond),
        jnp.logical_and(state.move_speed, state.ramp_index % 2),
    )
    move_speed = state.move_speed - move_speed_cond
    # 3. Update spawn_speed
    spawn_speed_cond = jnp.logical_and(
        jnp.logical_and(ramp_cond, 1 - timer_cond), state.spawn_speed > 1
    )
    spawn_speed = state.spawn_speed - spawn_speed_cond
    # 4. Update ramp_index
    ramp_index = state.ramp_index + jnp.logical_and(ramp_cond, 1 - timer_cond)
    return state.replace(
        spawn_timer=spawn_timer,
        move_timer=move_timer,
        ramp_timer=ramp_timer,
        move_speed=move_speed,
        spawn_speed=spawn_speed,
        ramp_index=ramp_index,
    )

