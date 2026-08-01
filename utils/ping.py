
def ping(
    request, timeout=_METADATA_DEFAULT_TIMEOUT, retry_count=_METADATA_DETECT_RETRIES
):
    """Checks to see if the metadata server is available.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        timeout (int): How long to wait for the metadata server to respond.
        retry_count (int): How many times to attempt connecting to metadata
            server using above timeout.

    Returns:
        bool: True if the metadata server is reachable, False otherwise.
    """
    use_mtls = _mtls.should_use_mds_mtls()
    _prepare_request_for_mds(request, use_mtls=use_mtls)
    # NOTE: The explicit ``timeout`` is a workaround. The underlying
    #       issue is that resolving an unknown host on some networks will take
    #       20-30 seconds; making this timeout short fixes the issue, but
    #       could lead to false negatives in the event that we are on GCE, but
    #       the metadata resolution was particularly slow. The latter case is
    #       "unlikely".
    headers = _METADATA_HEADERS.copy()
    headers[metrics.API_CLIENT_HEADER] = metrics.mds_ping()

    backoff = ExponentialBackoff(total_attempts=retry_count)

    for attempt in backoff:
        try:
            response = request(
                url=_get_metadata_ip_root(use_mtls),
                method="GET",
                headers=headers,
                timeout=timeout,
            )

            metadata_flavor = response.headers.get(_METADATA_FLAVOR_HEADER)
            return (
                response.status == http_client.OK
                and metadata_flavor == _METADATA_FLAVOR_VALUE
            )

        except exceptions.TransportError as e:
            _LOGGER.warning(
                "Compute Engine Metadata server unavailable on "
                "attempt %s of %s. Reason: %s",
                attempt,
                retry_count,
                e,
            )

    return False

