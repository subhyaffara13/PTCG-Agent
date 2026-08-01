
def reflect_on_borders(state: EnvState, height: int) -> EnvState:
    """Reflect ball at the bottom/top border of the frame."""
    # these are not really used?
    #   reflect_bottom = state.ball_position[0] < 0
    #   ball_position = jax.lax.select(
    #       reflect_bottom,
    #       state.ball_position.at[0].set(state.ball_position[0] * -1),
    #       state.ball_position,
    #   )
    #   ball_velocity = jax.lax.select(
    #       reflect_bottom,
    #       state.ball_velocity.at[0].set(state.ball_velocity[0] * -1),
    #       state.ball_velocity,
    #   )

    reflect_top = state.ball_position[0] >= height
    ball_position = jax.lax.select(
        reflect_top,
        state.ball_position.at[0].set(2 * (height - 1) - state.ball_position[0]),
        state.ball_position,
    )
    ball_velocity = jax.lax.select(
        reflect_top,
        state.ball_velocity.at[0].set(state.ball_velocity[0] * -1),
        state.ball_velocity,
    )
    return state.replace(ball_position=ball_position, ball_velocity=ball_velocity)

