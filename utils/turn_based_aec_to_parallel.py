from typing import Optional

def turn_based_aec_to_parallel(
    aec_env: AECEnv[AgentID, ObsType, Optional[ActionType]]
) -> ParallelEnv[AgentID, ObsType, Optional[ActionType]]:
    if isinstance(aec_env, parallel_to_aec_wrapper):
        return aec_env.env
    else:
        par_env = turn_based_aec_to_parallel_wrapper(aec_env)
        return par_env

