
def _is_rate_limit_error(exception) -> bool:
    """
    Checks if an exception is a RateLimitError that warrants a context reduction retry.
    This checks for both OpenAI's specific error and the generic HTTP 429 status code.
    """
    is_openai_rate_limit = "RateLimitError" in str(type(exception))
    is_http_429 = hasattr(exception, "status_code") and exception.status_code == 429
    return is_openai_rate_limit or is_http_429

