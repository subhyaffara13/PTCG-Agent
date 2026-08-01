
def to_parallel(
    aec_env: AECEnv[AgentID, ObsType, ActionType]
) -> ParallelEnv[AgentID, ObsType, ActionType]:
    warnings.warn(
        "The `to_parallel` function is deprecated. Use the `aec_to_parallel` function instead."
    )
    return aec_to_parallel(aec_env)

