from typing import Any, Union

def send_message(
    a2a_client: "A2AClientType",
    request: "SendMessageRequest",
    **kwargs: Any,
) -> Union[LiteLLMSendMessageResponse, Coroutine[Any, Any, LiteLLMSendMessageResponse]]:
    """
    Sync: Send a message to an A2A agent.

    Uses the @client decorator for LiteLLM logging and tracking.

    Args:
        a2a_client: An initialized a2a.client.A2AClient instance
        request: SendMessageRequest from a2a.types
        **kwargs: Additional arguments passed to the client decorator

    Returns:
        LiteLLMSendMessageResponse (wraps a2a SendMessageResponse with _hidden_params)
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        return asend_message(a2a_client=a2a_client, request=request, **kwargs)
    else:
        return asyncio.run(
            asend_message(a2a_client=a2a_client, request=request, **kwargs)
        )

