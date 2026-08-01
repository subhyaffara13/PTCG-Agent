
def from_parallel(
    par_env: ParallelEnv[AgentID, ObsType, Optional[ActionType]]
) -> AECEnv[AgentID, ObsType, Optional[ActionType]]:
    warnings.warn(
        "The `from_parallel` function is deprecated. Use the `parallel_to_aec` function instead."
    )
    return parallel_to_aec(par_env)

