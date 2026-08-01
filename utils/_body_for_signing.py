
def _body_for_signing(request: httpx.Request) -> bytes:
    try:
        return request.content
    except httpx.RequestNotRead as exc:
        raise OpenAIError(
            "Bedrock SigV4 authentication requires a replayable request body. "
            "Buffer the body before sending or use bearer authentication."
        ) from exc

