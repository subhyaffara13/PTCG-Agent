from typing import Tuple

def step_ball_brick(
    state: EnvState, new_x: jnp.ndarray, new_y: jnp.ndarray
) -> Tuple[EnvState, jnp.ndarray]:
    """Helper that computes reward and termination cond. from brickmap."""

    reward = 0

    # Reflect ball direction if bounced off at y border
    border_cond1_y = new_y < 0
    new_y = lax.select(border_cond1_y, 0, new_y)
    ball_dir = lax.select(
        border_cond1_y, jnp.array([3, 2, 1, 0])[state.ball_dir], state.ball_dir
    )

    # 1st NASTY ELIF BEGINS HERE... = Brick collision
    strike_toggle = jnp.logical_and(
        1 - border_cond1_y, state.brick_map[new_y, new_x] == 1
    )
    strike_bool = jnp.logical_and((1 - state.strike), strike_toggle)
    reward += strike_bool * 1.0
    # next line wasn't used anywhere
    # strike = jax.lax.select(strike_toggle, strike_bool, False)

    brick_map = jax.lax.select(
        strike_bool, state.brick_map.at[new_y, new_x].set(0), state.brick_map
    )
    new_y = jax.lax.select(strike_bool, state.last_y, new_y)
    ball_dir = jax.lax.select(strike_bool, jnp.array([3, 2, 1, 0])[ball_dir], ball_dir)

    # 2nd NASTY ELIF BEGINS HERE... = Wall collision
    brick_cond = jnp.logical_and(1 - strike_toggle, new_y == 9)

    # Spawn new bricks if there are no more around - everything is collected
    spawn_bricks = jnp.logical_and(brick_cond, jnp.count_nonzero(brick_map) == 0)
    brick_map = jax.lax.select(spawn_bricks, brick_map.at[1:4, :].set(1), brick_map)

    # Redirect ball because it collided with old player position
    redirect_ball1 = jnp.logical_and(brick_cond, state.ball_x == state.pos)
    ball_dir = jax.lax.select(
        redirect_ball1, jnp.array([3, 2, 1, 0])[ball_dir], ball_dir
    )
    new_y = jax.lax.select(redirect_ball1, state.last_y, new_y)

    # Redirect ball because it collided with new player position
    redirect_ball2a = jnp.logical_and(brick_cond, 1 - redirect_ball1)
    redirect_ball2 = jnp.logical_and(redirect_ball2a, new_x == state.pos)
    ball_dir = jax.lax.select(
        redirect_ball2, jnp.array([2, 3, 0, 1])[ball_dir], ball_dir
    )
    new_y = jax.lax.select(redirect_ball2, state.last_y, new_y)
    redirect_cond = jnp.logical_and(1 - redirect_ball1, 1 - redirect_ball2)
    terminal = jnp.logical_and(brick_cond, redirect_cond)

    strike = jax.lax.select(1 - strike_toggle == 1, False, True)
    return (
        state.replace(
            ball_dir=ball_dir,
            brick_map=brick_map,
            strike=strike,
            ball_x=new_x,
            ball_y=new_y,
            terminal=terminal,
        ),
        reward,
    )

