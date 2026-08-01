
def _set_agent_id_on_logging_obj(
    kwargs: Dict[str, Any],
    agent_id: Optional[str],
) -> None:
    """
    Set agent_id on litellm_logging_obj for SpendLogs tracking.

    Args:
        kwargs: The kwargs dict containing litellm_logging_obj
        agent_id: The A2A agent ID
    """
    if agent_id is None:
        return

    litellm_logging_obj = kwargs.get("litellm_logging_obj")
    if litellm_logging_obj is not None:
        # Set agent_id directly on model_call_details (same pattern as custom_llm_provider)
        litellm_logging_obj.model_call_details["agent_id"] = agent_id

