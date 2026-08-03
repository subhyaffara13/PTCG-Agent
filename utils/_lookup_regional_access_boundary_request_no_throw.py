import json

def _lookup_regional_access_boundary_request_no_throw(
    request, url, can_retry=True, headers=None, fail_fast=False
):
    """Makes a request to the Regional Access Boundary lookup endpoint. This
        function doesn't throw on response errors.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        url (str): The Regional Access Boundary lookup url.
        can_retry (bool): Enable or disable request retry behavior. Defaults to true.
        headers (Optional[Mapping[str, str]]): The headers for the request.
        fail_fast (bool): Whether the lookup should fail fast (uses a short timeout and no retries).

    Returns:
        Tuple(bool, Mapping[str, str], Optional[bool]): A boolean indicating
          if the request is successful, a mapping for the JSON-decoded response
          data and in the case of an error a boolean indicating if the error
          is retryable.
    """

    response_data = {}
    retryable_error = False

    timeout = _BLOCKING_REGIONAL_ACCESS_BOUNDARY_LOOKUP_TIMEOUT if fail_fast else None
    total_attempts = 1 if fail_fast else 6
    retries = _exponential_backoff.ExponentialBackoff(total_attempts=total_attempts)

    for _ in retries:
        response = request(method="GET", url=url, headers=headers, timeout=timeout)
        response_body = (
            response.data.decode("utf-8")
            if hasattr(response.data, "decode")
            else response.data
        )

        try:
            # response_body should be a JSON
            response_data = json.loads(response_body)
        except ValueError:
            response_data = response_body

        if response.status == http_client.OK:
            return True, response_data, None

        retryable_error = _can_retry(
            status_code=response.status, response_data=response_data
        )
        # Add 502 (Bad Gateway) as a retryable error for RAB lookups.
        if response.status == http_client.BAD_GATEWAY:
            retryable_error = True

        if not can_retry or not retryable_error:
            return False, response_data, retryable_error

    return False, response_data, retryable_error

