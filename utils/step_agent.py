from typing import Tuple

def step_agent(state: EnvState, action: jnp.ndarray) -> EnvState:
    """Update the position of the agent."""
    # Resolve player action via implicit conditional updates of coordinates
    player_x = (
        jnp.maximum(0, state.player_x - 1) * (action == 1)  # l
        + jnp.minimum(9, state.player_x + 1) * (action == 3)  # r
        + state.player_x * jnp.logical_and(action != 1, action != 3)
    )  # others

    player_y = (
        jnp.maximum(1, state.player_y - 1) * (action == 2)  # u
        + jnp.minimum(8, state.player_y + 1) * (action == 4)  # d
        + state.player_y * jnp.logical_and(action != 2, action != 4)
    )  # others
    return state.replace(player_x=player_x, player_y=player_y)


def step_agent(
    state: EnvState,
    action: jnp.ndarray,
) -> Tuple[EnvState, jnp.ndarray, jnp.ndarray]:
    """Helper that steps the agent and checks boundary conditions."""
    # Update player position
    pos = (
        # Action left & border condition
        jnp.maximum(0, state.pos - 1) * (action == 1)
        # Action right & border condition
        + jnp.minimum(9, state.pos + 1) * (action == 3)
        # Don't move player if not l/r chosen
        + state.pos * jnp.logical_and(action != 1, action != 3)
    )

    # Update ball position - based on direction of movement
    last_x = state.ball_x
    last_y = state.ball_y
    new_x = (
        (state.ball_x - 1) * (state.ball_dir == 0)
        + (state.ball_x + 1) * (state.ball_dir == 1)
        + (state.ball_x + 1) * (state.ball_dir == 2)
        + (state.ball_x - 1) * (state.ball_dir == 3)
    )
    new_y = (
        (state.ball_y - 1) * (state.ball_dir == 0)
        + (state.ball_y - 1) * (state.ball_dir == 1)
        + (state.ball_y + 1) * (state.ball_dir == 2)
        + (state.ball_y + 1) * (state.ball_dir == 3)
    )

    # Boundary conditions for x position
    border_cond_x = jnp.logical_or(new_x < 0, new_x > 9)
    new_x = jax.lax.select(border_cond_x, (0 * (new_x < 0) + 9 * (new_x > 9)), new_x)
    # Reflect ball direction if bounced off at x border
    ball_dir = jax.lax.select(
        border_cond_x, jnp.array([1, 0, 3, 2])[state.ball_dir], state.ball_dir
    )
    return (
        state.replace(
            pos=pos,
            last_x=last_x,
            last_y=last_y,
            ball_dir=ball_dir,
        ),
        new_x,
        new_y,
    )


def step_agent(
    action: jnp.ndarray, state: EnvState, params: EnvParams
) -> Tuple[EnvState, jnp.ndarray, bool]:
    """Perform 1st part of step transition for agent."""
    cond_up = jnp.logical_and(action == 2, state.move_timer == 0)
    cond_down = jnp.logical_and(action == 4, state.move_timer == 0)
    any_cond = jnp.logical_or(cond_up, cond_down)
    state_up = jnp.maximum(0, state.pos - 1)
    state_down = jnp.minimum(9, state.pos + 1)
    pos = (1 - any_cond) * state.pos + cond_up * state_up + cond_down * state_down
    move_timer = jax.lax.select(any_cond, params.player_speed, state.move_timer)
    # Check win cond. - increase reward, randomize cars, reset agent position
    win_cond = pos == 0
    reward = win_cond * 1.0
    pos = jax.lax.select(win_cond, 9, pos)
    return state.replace(pos=pos, move_timer=move_timer), reward, win_cond.item()


def step_agent(action: jnp.ndarray, state: EnvState, params: EnvParams) -> EnvState:
    """Resolve player action - fire, left, right."""
    fire_cond = jnp.logical_and(action == 5, state.shot_timer == 0)
    left_cond, right_cond = (action == 1), (action == 3)
    f_bullet_map = jax.lax.select(
        fire_cond,
        state.f_bullet_map.at[9, state.pos].set(1),
        state.f_bullet_map,
    )
    shot_timer = jax.lax.select(fire_cond, params.shot_cool_down, state.shot_timer)

    # Update position of agent
    pos = jax.lax.select(left_cond, jnp.maximum(0, state.pos - 1), state.pos)
    pos = jax.lax.select(right_cond, jnp.minimum(9, pos + 1), pos)

    # Update Friendly Bullets and Enemy Bullets
    f_bullet_map = jnp.roll(f_bullet_map, -1, axis=0)
    f_bullet_map = f_bullet_map.at[9, :].set(0)

    e_bullet_map = jnp.roll(state.e_bullet_map, 1, axis=0)
    e_bullet_map = e_bullet_map.at[0, :].set(0)

    # Check for terminal collision
    bullet_terminal = e_bullet_map[9, state.pos]
    terminal = jnp.logical_or(state.terminal, bullet_terminal)
    return state.replace(
        pos=pos,
        f_bullet_map=f_bullet_map,
        e_bullet_map=e_bullet_map,
        shot_timer=shot_timer,
        terminal=terminal,
    )

