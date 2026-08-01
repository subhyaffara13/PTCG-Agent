
def aec_to_parallel(
    aec_env: AECEnv[AgentID, ObsType, ActionType]
) -> ParallelEnv[AgentID, ObsType, ActionType]:
    """Converts an AEC environment to a Parallel environment.

    In the case of an existing Parallel environment wrapped using a `parallel_to_aec_wrapper`, this function will return the original Parallel environment.
    Otherwise, it will apply the `aec_to_parallel_wrapper` to convert the environment.
    """
    if isinstance(aec_env, OrderEnforcingWrapper) and isinstance(
        aec_env.env, parallel_to_aec_wrapper
    ):
        return aec_env.env.env
    else:
        par_env = aec_to_parallel_wrapper(aec_env)
        return par_env

