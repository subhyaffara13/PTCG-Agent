
def _state_api_key(state: _LegacyBedrockState) -> str:
    return state.explicit_api_key or (state.environment_bearer_token if state.uses_environment_bearer else "") or ""

