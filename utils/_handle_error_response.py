import json

def _handle_error_response(response_data, retryable_error):
    """Translates an error response into an exception.

    Args:
        response_data (Mapping | str): The decoded response data.
        retryable_error Optional[bool]: A boolean indicating if an error is retryable.
            Defaults to False.

    Raises:
        google.auth.exceptions.RefreshError: The errors contained in response_data.
    """

    retryable_error = retryable_error if retryable_error else False

    if isinstance(response_data, str):
        raise exceptions.RefreshError(response_data, retryable=retryable_error)
    try:
        error_details = "{}: {}".format(
            response_data["error"], response_data.get("error_description")
        )
    # If no details could be extracted, use the response data.
    except (KeyError, ValueError):
        error_details = json.dumps(response_data)

    raise exceptions.RefreshError(
        error_details, response_data, retryable=retryable_error
    )

