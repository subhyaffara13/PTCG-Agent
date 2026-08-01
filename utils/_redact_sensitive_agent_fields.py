
def _redact_sensitive_agent_fields(
    agents: List[AgentResponse],
) -> List[AgentResponse]:
    """
    Return copies of the given agents with sensitive configuration fields
    redacted.  The original objects are not modified.
    """
    redacted: List[AgentResponse] = []
    for agent in agents:
        copy = agent.model_copy(deep=True)
        copy.static_headers = None
        copy.extra_headers = None
        if copy.litellm_params:
            copy.litellm_params = _get_masked_values(
                copy.litellm_params,
                unmasked_length=4,
                number_of_asterisks=4,
            )
        redacted.append(copy)
    return redacted

