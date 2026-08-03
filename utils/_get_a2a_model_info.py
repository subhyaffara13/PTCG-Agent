from typing import Any, Dict

def _get_a2a_model_info(a2a_client: Any, kwargs: Dict[str, Any]) -> str:
    """
    Extract agent info and set model/custom_llm_provider for cost tracking.

    Sets model info on the litellm_logging_obj if available.
    Returns the agent name for logging.
    """
    agent_name = "unknown"

    # Try to get agent card from our stored attribute first, then fallback to SDK attribute
    agent_card = getattr(a2a_client, "_litellm_agent_card", None)
    if agent_card is None:
        agent_card = getattr(a2a_client, "agent_card", None)

    if agent_card is not None:
        agent_name = getattr(agent_card, "name", "unknown") or "unknown"

    # Build model string
    model = f"a2a_agent/{agent_name}"
    custom_llm_provider = "a2a_agent"

    # Set on litellm_logging_obj if available (for standard logging payload)
    litellm_logging_obj = kwargs.get("litellm_logging_obj")
    if litellm_logging_obj is not None:
        litellm_logging_obj.model = model
        litellm_logging_obj.custom_llm_provider = custom_llm_provider
        litellm_logging_obj.model_call_details["model"] = model
        litellm_logging_obj.model_call_details["custom_llm_provider"] = (
            custom_llm_provider
        )

    return agent_name

