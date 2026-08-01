
def _lookup_regional_access_boundary_request(
    request, url, can_retry=True, headers=None, fail_fast=False
):
    """Makes a request to the Regional Access Boundary lookup endpoint.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        url (str): The Regional Access Boundary lookup url.
        can_retry (bool): Enable or disable request retry behavior. Defaults to true.
        headers (Optional[Mapping[str, str]]): The headers for the request.
        fail_fast (bool): Whether the lookup should fail fast (uses a short timeout and no retries).

    Returns:
        Optional[Mapping[str, str]]: The JSON-decoded response data on success, or None on failure.
    """
    (
        response_status_ok,
        response_data,
        retryable_error,
    ) = _lookup_regional_access_boundary_request_no_throw(
        request, url, can_retry=can_retry, headers=headers, fail_fast=fail_fast
    )
    if not response_status_ok:
        _LOGGER.debug(
            "Regional Access Boundary HTTP request failed after retries: response_data=%s, retryable_error=%s",
            response_data,
            retryable_error,
        )
        return None
    return response_data

