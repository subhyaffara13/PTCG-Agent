
def move_paddles(
    action: int,
    paddle_y_speed: int,
    state: EnvState,
    paddle_half_height: int,
    height: int,
    use_ai_policy: bool,
) -> EnvState:
    """Update paddle positions and clip at height borders."""
    paddle_direction = -1 * (action == 1) + 1 * (action == 2)
    paddle_step = paddle_direction * paddle_y_speed
    # NOTE: Different from reference - full paddle is visible
    # Calculate new center of P1 based on action
    new_center_p1 = jnp.clip(
        state.paddle_centers[0] + paddle_step,
        paddle_half_height,
        height - paddle_half_height - 1,
    )
    # Calculate new center of P2 based on same action
    # This means both players play 'same' policy
    new_center_self = jnp.clip(
        state.paddle_centers[1] + paddle_step,
        paddle_half_height,
        height - paddle_half_height - 1,
    )

    # Calculate new center of P2 based on 'AI' policy
    # Minimize distance to ball!
    dist_center_down = jnp.abs(
        state.ball_position[0]
        - jnp.clip(
            state.paddle_centers[1] + paddle_y_speed,
            paddle_half_height,
            height - paddle_half_height - 1,
        )
    )
    dist_center_up = jnp.abs(
        state.ball_position[0]
        - jnp.clip(
            state.paddle_centers[1] - paddle_y_speed,
            paddle_half_height,
            height - paddle_half_height - 1,
        )
    )
    ai_go_up = dist_center_up < dist_center_down
    new_center_ai = jnp.clip(
        state.paddle_centers[1]
        - ai_go_up * paddle_y_speed
        + (1 - ai_go_up) * paddle_y_speed,
        paddle_half_height,
        height - paddle_half_height - 1,
    )
    new_center_p2 = jax.lax.select(use_ai_policy, new_center_ai, new_center_self)

    new_centers = jnp.array([new_center_p1, new_center_p2])
    return state.replace(paddle_centers=new_centers)

