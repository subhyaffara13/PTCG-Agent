
def should_run_mock_completion(
    mock_response: Optional[Any],
    mock_tool_calls: Optional[Any],
    mock_timeout: Optional[Any],
) -> bool:
    if mock_response or mock_tool_calls or mock_timeout:
        return True
    return False

