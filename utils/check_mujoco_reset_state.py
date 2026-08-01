
def check_mujoco_reset_state(
    env: gymnasium.envs.mujoco.MujocoEnv,
    seed=1234,
    state_type: mujoco.mjtState = mujoco.mjtState.mjSTATE_INTEGRATION,
):
    """Asserts that `env.reset()` properly resets the state (not affected by previous steps).

    Note: assuming `check_reset_seed` has passed.

    Arguments:
        env: Environment which is being tested.
        seed: the `seed` used in `env.reset(seed)`.
        state_type: see the [documentation of mjtState](https://mujoco.readthedocs.io/en/stable/APIreference/APItypes.html#mjtstate).
    """
    env.action_space.seed(seed)
    action = env.action_space.sample()

    env.reset(seed=seed)
    first_reset_state = get_state(env, state_type)
    env.step(action)

    env.reset(seed=seed)
    second_reset_state = get_state(env, state_type)

    assert np.all(first_reset_state == second_reset_state), "reset is not deterministic"

