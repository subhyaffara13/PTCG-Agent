from typing import Tuple

def step_transition(
    state: EnvState, action_right: bool, right_cond: jnp.ndarray, size: int
) -> Tuple[jnp.ndarray, int, jnp.ndarray]:
    """Get the state transition for the selected action."""
    # Standard right path transition
    column = jax.lax.select(
        right_cond, jnp.clip(state.column + 1, 0, size - 1), state.column
    )

    # You were on the right path and went wrong
    right_wrong_cond = jnp.logical_and(1 - action_right, state.row == column)
    bad_episode = jax.lax.select(right_wrong_cond, True, state.bad_episode)
    column = jax.lax.select(
        action_right, column, jnp.clip(state.column - 1, 0, size - 1)
    )
    row = state.row + 1
    return column, row, bad_episode

