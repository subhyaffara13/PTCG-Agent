
def _handle_mock_timeout(
    mock_timeout: Optional[bool],
    timeout: Optional[Union[float, str, httpx.Timeout]],
    model: str,
):
    if mock_timeout is True and timeout is not None:
        _sleep_for_timeout(timeout)
        raise litellm.Timeout(
            message="This is a mock timeout error",
            llm_provider="openai",
            model=model,
        )

