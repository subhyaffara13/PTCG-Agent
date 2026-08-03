from typing import Tuple

def step_reward(
    state: EnvState,
    action_right: bool,
    right_cond: jnp.ndarray,
    rand_reward: jnp.ndarray,
    size: int,
    params: EnvParams,
) -> Tuple[jnp.ndarray, jnp.ndarray]:
    """Get the reward for the selected action."""
    reward = 0.0
    # Reward calculation.
    rew_cond = jnp.logical_and(state.column == size - 1, action_right)
    reward += rew_cond
    denoised_return = state.denoised_return + rew_cond

    # Noisy rewards on the 'end' of chain.
    col_at_edge = jnp.logical_or(state.column == 0, state.column == size - 1)
    chain_end = jnp.logical_and(state.row == size - 1, col_at_edge)
    det_chain_end = jnp.logical_and(chain_end, params.deterministic)
    reward += rand_reward * det_chain_end * (1 - params.deterministic)
    reward -= right_cond * params.unscaled_move_cost / size
    return reward, denoised_return

