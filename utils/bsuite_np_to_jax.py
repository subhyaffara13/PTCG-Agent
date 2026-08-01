
def bsuite_np_to_jax(env, env_name: str = "Catch-bsuite", get_jax: bool = False):
    """Collects env state of bsuite into dict for JAX `step`."""
    state_gym_to_jax = None
    if env_name == "Catch-bsuite":
        state_gym_to_jax = {
            "ball_x": env._ball_x,
            "ball_y": env._ball_y,
            "paddle_x": env._paddle_x,
            "paddle_y": env._paddle_y,
            "prev_done": env._reset_next_step,
            "time": 0,
        }
        if get_jax:

            return catch.EnvState(**state_gym_to_jax)
    elif env_name == "DeepSea-bsuite":
        state_gym_to_jax = {
            "row": env._row,
            "column": env._column,
            "bad_episode": env._bad_episode,
            "total_bad_episodes": env._total_bad_episodes,
            "denoised_return": env._denoised_return,
            "optimal_return": env._optimal_return,
            "action_mapping": env._action_mapping,
            "time": 0,
        }
        if get_jax:

            return deep_sea.EnvState(**state_gym_to_jax)
    elif env_name == "DiscountingChain-bsuite":
        state_gym_to_jax = {
            "rewards": env._rewards,
            "context": env._context,
            "time": env._timestep,
        }
        if get_jax:

            return discounting_chain.EnvState(**state_gym_to_jax)
    elif env_name == "MemoryChain-bsuite":
        state_gym_to_jax = {
            "context": env._context,
            "query": env._query,
            "total_perfect": env._total_perfect,
            "total_regret": env._total_regret,
            "time": env._timestep,
        }
        if get_jax:

            return memory_chain.EnvState(**state_gym_to_jax)
    elif env_name == "UmbrellaChain-bsuite":
        state_gym_to_jax = {
            "need_umbrella": env._need_umbrella,
            "has_umbrella": env._has_umbrella,
            "total_regret": env._total_regret,
            "time": env._timestep,
        }
        if get_jax:

            return umbrella_chain.EnvState(**state_gym_to_jax)
    elif env_name == "MNISTBandit-bsuite":
        state_gym_to_jax = {
            "correct_label": env._correct_label,
            "regret": env._total_regret,
            "time": 0,
        }
        if get_jax:

            return mnist.EnvState(**state_gym_to_jax)
    elif env_name == "SimpleBandit-bsuite":
        state_gym_to_jax = {
            "rewards": env._rewards,
            "total_regret": env._total_regret,
            "time": 0,
        }
        if get_jax:

            return bandit.EnvState(**state_gym_to_jax)
    return state_gym_to_jax

