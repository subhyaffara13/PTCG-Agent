from typing import Any

def handle_a2a_localhost_retry(
    error: A2ALocalhostURLError,
    agent_card: Any,
    a2a_client: "A2AClientType",
    is_streaming: bool = False,
) -> "A2AClientType":
    """
    Handle A2ALocalhostURLError by fixing the URL and creating a new client.

    This is called when we catch an A2ALocalhostURLError and want to retry
    with the corrected URL.

    Args:
        error: The localhost URL error
        agent_card: The agent card object to fix
        a2a_client: The current A2A client
        is_streaming: Whether this is a streaming request (for logging)

    Returns:
        A new A2A client with the fixed URL

    Raises:
        ImportError: If the A2A SDK is not installed
    """
    if not A2A_SDK_AVAILABLE or _A2AClient is None:
        raise ImportError(
            "A2A SDK is required for localhost retry handling. "
            "Install it with: pip install a2a"
        )

    request_type = "streaming " if is_streaming else ""
    verbose_logger.warning(
        f"A2A {request_type}request to '{error.localhost_url}' failed: {error.original_error}. "
        f"Agent card contains localhost/internal URL. "
        f"Retrying with base_url '{error.base_url}'."
    )

    # Fix the agent card URL
    fix_agent_card_url(agent_card, error.base_url)

    # Create a new client with the fixed agent card (transport caches URL)
    return _A2AClient(
        httpx_client=a2a_client._transport.httpx_client,  # type: ignore[union-attr]
        agent_card=agent_card,
    )

