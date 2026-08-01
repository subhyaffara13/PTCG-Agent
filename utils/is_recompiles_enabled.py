
def is_recompiles_enabled() -> bool:
    return torch._logging._internal.log_state.is_artifact_enabled("recompiles")

