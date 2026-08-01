
def step_aliens(state: EnvState) -> EnvState:
    """Update aliens - border and collision check."""
    alien_terminal_1 = state.alien_map[9, state.pos]
    alien_move_cond = state.alien_move_timer == 0

    alien_move_timer = jax.lax.select(
        alien_move_cond,
        jnp.minimum(jnp.count_nonzero(state.alien_map), state.enemy_move_interval),
        state.alien_move_timer,
    )
    cond1 = jnp.logical_and(jnp.sum(state.alien_map[:, 0]) > 0, state.alien_dir < 0)
    cond2 = jnp.logical_and(jnp.sum(state.alien_map[:, 9]) > 0, state.alien_dir > 0)
    alien_border_cond = jnp.logical_and(alien_move_cond, jnp.logical_or(cond1, cond2))
    alien_dir = jax.lax.select(alien_border_cond, -1 * state.alien_dir, state.alien_dir)
    alien_terminal_2 = jnp.logical_and(
        alien_border_cond, jnp.sum(state.alien_map[9, :]) > 0
    )
    alien_map = jax.lax.select(
        alien_move_cond,
        (
            jax.lax.select(
                alien_border_cond,
                jnp.roll(state.alien_map, 1, axis=0),
                jnp.roll(state.alien_map, alien_dir, axis=1),
            )
        ),
        state.alien_map,
    )
    alien_terminal_3 = jnp.logical_and(alien_move_cond, alien_map[9, state.pos])

    # Jointly evaluate the 3 alien terminal conditions
    alien_terminal = (alien_terminal_1 + alien_terminal_2 + alien_terminal_3) > 0
    terminal = jnp.logical_or(state.terminal, alien_terminal)
    return state.replace(
        alien_move_timer=alien_move_timer,
        alien_dir=alien_dir,
        alien_map=alien_map,
        terminal=terminal,
    )

