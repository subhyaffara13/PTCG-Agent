from typing import Optional

def parallel_to_aec(
    par_env: ParallelEnv[AgentID, ObsType, Optional[ActionType]]
) -> AECEnv[AgentID, ObsType, Optional[ActionType]]:
    """Converts a Parallel environment to an AEC environment.

    In the case of an existing AEC environment wrapped using a `aec_to_parallel_wrapper`, this function will return the original AEC environment.
    Otherwise, it will apply the `parallel_to_aec_wrapper` to convert the environment.
    """
    if isinstance(par_env, aec_to_parallel_wrapper):
        return par_env.aec_env
    else:
        aec_env = parallel_to_aec_wrapper(par_env)
        ordered_env = OrderEnforcingWrapper(aec_env)
        return ordered_env

