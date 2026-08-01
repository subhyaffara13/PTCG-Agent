
def step_shoot(state: EnvState, params: EnvParams) -> Tuple[EnvState, jnp.ndarray]:
    """Update aliens - shooting check and calculate rewards."""
    reward = 0
    alien_shot_cond = state.alien_shot_timer == 0
    alien_shot_timer = jax.lax.select(
        alien_shot_cond, params.enemy_shot_interval, state.alien_shot_timer
    )

    # nearest_alien has 3 outputs used to update map: [alien_exists, loc, id]
    alien_exists, loc, idx = get_nearest_alien(state.pos, state.alien_map)
    update_aliens_cond = jnp.logical_and(alien_shot_cond, alien_exists)
    e_bullet_map = jax.lax.select(
        update_aliens_cond,
        state.e_bullet_map.at[loc, idx].set(1),
        state.e_bullet_map,
    )
    kill_locations = jnp.logical_and(
        state.alien_map, state.alien_map == state.f_bullet_map
    )

    # Compute reward based on killed aliens
    reward += jnp.sum(kill_locations)
    # Delete aliens/bullets based on kill_locations elementwise multiplication
    alien_map = state.alien_map * (1 - kill_locations)
    f_bullet_map = state.f_bullet_map * (1 - kill_locations)
    return (
        state.replace(
            alien_shot_timer=alien_shot_timer,
            e_bullet_map=e_bullet_map,
            alien_map=alien_map,
            f_bullet_map=f_bullet_map,
        ),
        reward,
    )

