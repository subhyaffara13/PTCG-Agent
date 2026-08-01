
def update_game_state(state: EnvState, width: int) -> jnp.ndarray:
    """Check if right or left border win conditions are met."""
    win_right = state.ball_position[1] < 0
    win_left = state.ball_position[1] >= width
    return jnp.logical_or(win_right, win_left)

