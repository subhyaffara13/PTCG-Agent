
def _can_retry(status_code, response_data):
    """Checks if a request can be retried by inspecting the status code
    and response body of the request.

    Args:
        status_code (int): The response status code.
        response_data (Mapping | str): The decoded response data.

    Returns:
      bool: True if the response is retryable. False otherwise.
    """
    if status_code in transport.DEFAULT_RETRYABLE_STATUS_CODES:
        return True

    try:
        # For a failed response, response_body could be a string
        error_desc = response_data.get("error_description") or ""
        error_code = response_data.get("error") or ""

        if not isinstance(error_code, str) or not isinstance(error_desc, str):
            return False

        # Per Oauth 2.0 RFC https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.2.1
        # This is needed because a redirect will not return a 500 status code.
        retryable_error_descriptions = {
            "internal_failure",
            "server_error",
            "temporarily_unavailable",
        }

        if any(e in retryable_error_descriptions for e in (error_code, error_desc)):
            return True

    except AttributeError:
        pass

    return False

