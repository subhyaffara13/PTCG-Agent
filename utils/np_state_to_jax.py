
def np_state_to_jax(env, env_name: str = "Pendulum-v1", get_jax: bool = False):
    """Helper that collects env state into dict for JAX `step`."""

    if env_name in [
        "Pendulum-v1",
        "CartPole-v1",
        "MountainCar-v0",
        "MountainCarContinuous-v0",
        "Acrobot-v1",
    ]:
        state_gym_to_jax = control_np_to_jax(env, env_name, get_jax)
    elif env_name in [
        "Catch-bsuite",
        "DeepSea-bsuite",
        "DiscountingChain-bsuite",
        "MemoryChain-bsuite",
        "UmbrellaChain-bsuite",
        "MNISTBandit-bsuite",
        "SimpleBandit-bsuite",
    ]:
        state_gym_to_jax = bsuite_np_to_jax(env, env_name, get_jax)
    elif env_name in [
        "Asterix-MinAtar",
        "Breakout-MinAtar",
        "Freeway-MinAtar",
        # "Seaquest-MinAtar",
        "SpaceInvaders-MinAtar",
    ]:
        state_gym_to_jax = minatar_np_to_jax(env, env_name, get_jax)
    else:
        raise ValueError(f"{env_name} is not in set of implemented environments.")
    return state_gym_to_jax

