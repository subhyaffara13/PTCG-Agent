
def reflect_on_paddle(
    state: EnvState, width: int, paddle_half_height: int, env_params: EnvParams
):
    """Reflect ball on paddle contact."""
    left_paddle_reflected_x = 2 * 1 - state.ball_position[1]
    right_paddle_reflected_x = 2 * (width - 2) - state.ball_position[1]

    paddle_height_distance = state.ball_position[jnp.newaxis, 0] - state.paddle_centers

    left_paddle_hit = jnp.logical_and(
        left_paddle_reflected_x >= 1,
        jnp.fabs(paddle_height_distance[0]) <= paddle_half_height,
    )
    right_paddle_hit = jnp.logical_and(
        right_paddle_reflected_x < width - 2,
        jnp.fabs(paddle_height_distance[1]) < paddle_half_height + 1,
    )

    # Left paddle hit updates
    left_ball_position = state.ball_position.at[1].set(left_paddle_reflected_x)
    left_ball_velocity = state.ball_velocity.at[1].set(state.ball_velocity[1] * -1)
    left_ball_velocity = left_ball_velocity.at[0].set(
        jnp.clip(
            left_ball_velocity[0] + paddle_height_distance[0] / paddle_half_height,
            -env_params.ball_max_y_speed,
            env_params.ball_max_y_speed,
        )
    )
    ball_position = jax.lax.select(
        left_paddle_hit, left_ball_position, state.ball_position
    )
    ball_velocity = jax.lax.select(
        left_paddle_hit, left_ball_velocity, state.ball_velocity
    )

    # Right paddle hit updates
    right_ball_position = ball_position.at[1].set(right_paddle_reflected_x)
    right_ball_velocity = ball_velocity.at[1].set(ball_velocity[1] * -1)
    right_ball_velocity = right_ball_velocity.at[0].set(
        jnp.clip(
            right_ball_velocity[0] + paddle_height_distance[1] / paddle_half_height,
            -env_params.ball_max_y_speed,
            env_params.ball_max_y_speed,
        )
    )
    ball_position = jax.lax.select(right_paddle_hit, right_ball_position, ball_position)
    ball_velocity = jax.lax.select(right_paddle_hit, right_ball_velocity, ball_velocity)
    return state.replace(
        ball_position=ball_position,
        ball_velocity=ball_velocity,
    )

