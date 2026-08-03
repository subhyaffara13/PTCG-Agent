from typing import Optional, Union

def _handle_mock_potential_exceptions(
    mock_response: Union[str, Exception],
    model: str,
    custom_llm_provider: Optional[str] = None,
):
    if isinstance(mock_response, Exception):
        if isinstance(mock_response, openai.APIError):
            raise mock_response
        raise litellm.MockException(
            status_code=getattr(mock_response, "status_code", 500),  # type: ignore
            message=getattr(mock_response, "text", str(mock_response)),
            llm_provider=getattr(
                mock_response, "llm_provider", custom_llm_provider or "openai"
            ),  # type: ignore
            model=model,  # type: ignore
            request=httpx.Request(method="POST", url="https://api.openai.com/v1/"),
        )
    elif isinstance(mock_response, str) and mock_response == "litellm.RateLimitError":
        raise litellm.RateLimitError(
            message="this is a mock rate limit error",
            llm_provider=getattr(
                mock_response, "llm_provider", custom_llm_provider or "openai"
            ),  # type: ignore
            model=model,
        )
    elif (
        isinstance(mock_response, str)
        and mock_response == "litellm.ContextWindowExceededError"
    ):
        raise litellm.ContextWindowExceededError(
            message="this is a mock context window exceeded error",
            llm_provider=getattr(
                mock_response, "llm_provider", custom_llm_provider or "openai"
            ),  # type: ignore
            model=model,
        )
    elif (
        isinstance(mock_response, str)
        and mock_response == "litellm.InternalServerError"
    ):
        raise litellm.InternalServerError(
            message="this is a mock internal server error",
            llm_provider=getattr(
                mock_response, "llm_provider", custom_llm_provider or "openai"
            ),  # type: ignore
            model=model,
        )
    elif isinstance(mock_response, str) and mock_response.startswith(
        "Exception: content_filter_policy"
    ):
        raise litellm.MockException(
            status_code=400,
            message=mock_response,
            llm_provider="azure",
            model=model,  # type: ignore
            request=httpx.Request(method="POST", url="https://api.openai.com/v1/"),
        )

