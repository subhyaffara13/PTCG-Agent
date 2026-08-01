
def move_ball(state: EnvState) -> EnvState:
    """Update ball position using velocity."""
    ball_position = state.ball_position + state.ball_velocity
    return state.replace(ball_position=ball_position)

