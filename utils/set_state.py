
def set_state(state):
    """
    A context manager that sets the state of the backends to one returned by :obj:`get_state`.

    See Also
    --------
    get_state
        Gets a state to be set by this context manager.
    """  # noqa: E501
    old_state = get_state()
    _uarray.set_state(state)
    try:
        yield
    finally:
        _uarray.set_state(old_state, True)


def set_state(
    env: gymnasium.envs.mujoco.MujocoEnv,
    state: np.ndarray,
    state_type: mujoco.mjtState = mujoco.mjtState.mjSTATE_FULLPHYSICS,
):
    """Set the state of `env`.

    Arguments:
        env: Environment whose state to set, `env.model` & `env.data` must be accessible.
        state: State to set (generated from get_state).
        state_type: see the [documentation of mjtState](https://mujoco.readthedocs.io/en/stable/APIreference/APItypes.html#mjtstate) most users can use the default for training purposes or `mujoco.mjtState.mjSTATE_INTEGRATION` for validation purposes.
    """
    assert mujoco.__version__ >= "2.3.6", "Feature requires `mujoco>=2.3.6`"

    mujoco.mj_setState(
        env.unwrapped.model,
        env.unwrapped.data,
        state,
        spec=state_type,
    )
    return state

