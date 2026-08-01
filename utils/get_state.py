
def get_state():
    """
    Returns an opaque object containing the current state of all the backends.

    Can be used for synchronization between threads/processes.

    See Also
    --------
    set_state
        Sets the state returned by this function.
    """
    return _uarray.get_state()


def get_state(
    env: gymnasium.envs.mujoco.MujocoEnv,
    state_type: mujoco.mjtState = mujoco.mjtState.mjSTATE_FULLPHYSICS,
):
    """Gets the state of `env`.

    Arguments:
        env: Environment whose state to copy, `env.model` & `env.data` must be accessible.
        state_type: see the [documentation of mjtState](https://mujoco.readthedocs.io/en/stable/APIreference/APItypes.html#mjtstate) most users can use the default for training purposes or `mujoco.mjtState.mjSTATE_INTEGRATION` for validation purposes.
    """
    assert mujoco.__version__ >= "2.3.6", "Feature requires `mujoco>=2.3.6`"

    state = np.empty(mujoco.mj_stateSize(env.unwrapped.model, state_type))
    mujoco.mj_getState(env.unwrapped.model, env.unwrapped.data, state, state_type)
    return state

