
def _lookup_regional_access_boundary(request, url, headers=None, fail_fast=False):
    """Implements the global lookup of a credential Regional Access Boundary.
    For the lookup, we send a request to the global lookup endpoint and then
    parse the response. Service account credentials, workload identity
    pools and workforce pools implementation may have Regional Access Boundaries configured.
    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        url (str): The Regional Access Boundary lookup url.
        headers (Optional[Mapping[str, str]]): The headers for the request.
        fail_fast (bool): Whether the lookup should fail fast (uses a short timeout and no retries).
    Returns:
        Optional[Mapping[str,list|str]]: A dictionary containing
            "locations" as a list of allowed locations as strings and
            "encodedLocations" as a hex string.
            e.g:
            {
                "locations": [
                    "us-central1", "us-east1", "europe-west1", "asia-east1"
                ],
                "encodedLocations": "0xA30"
            }
    """

    response_data = _lookup_regional_access_boundary_request(
        request, url, headers=headers, fail_fast=fail_fast
    )
    if response_data is None:
        # Error was already logged by _lookup_regional_access_boundary_request
        return None

    if not isinstance(response_data, dict) or "encodedLocations" not in response_data:
        _LOGGER.error(
            "Regional Access Boundary response malformed: missing 'encodedLocations' key in %s",
            response_data,
        )
        return None
    return response_data

