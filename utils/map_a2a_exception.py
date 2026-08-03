from typing import Optional

def map_a2a_exception(
    original_exception: Exception,
    card_url: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
) -> Exception:
    """
    Map an A2A SDK exception to a LiteLLM A2A exception type.

    Args:
        original_exception: The original exception from the A2A SDK
        card_url: The URL from the agent card (if available)
        api_base: The original API base URL
        model: The model/agent name

    Returns:
        A mapped LiteLLM A2A exception

    Raises:
        A2ALocalhostURLError: If the error is a connection error to a localhost URL
        A2AConnectionError: If the error is a general connection error
        A2AAgentCardError: If the error is related to agent card issues
        A2AError: For other A2A-related errors
    """
    error_str = str(original_exception)

    # Check for localhost URL connection error (special case - retryable)
    if (
        card_url
        and api_base
        and A2AExceptionCheckers.is_localhost_url(card_url)
        and A2AExceptionCheckers.is_connection_error(error_str)
    ):
        raise A2ALocalhostURLError(
            localhost_url=card_url,
            base_url=api_base,
            original_error=original_exception,
            model=model,
        )

    # Check for agent card errors
    if A2AExceptionCheckers.is_agent_card_error(error_str):
        raise A2AAgentCardError(
            message=error_str,
            url=api_base,
            model=model,
        )

    # Check for general connection errors
    if A2AExceptionCheckers.is_connection_error(error_str):
        raise A2AConnectionError(
            message=error_str,
            url=card_url or api_base,
            model=model,
        )

    # Default: wrap in generic A2AError
    raise A2AError(
        message=error_str,
        model=model,
    )

