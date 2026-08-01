
def _prepare_request_for_mds(request, use_mtls=False) -> None:
    """Prepares a request for the metadata server.

    This will check if mTLS should be used and mount the mTLS adapter if needed.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests. If mTLS is enabled, and the request supports sessions,
            the request will have the mTLS adapter mounted. Otherwise, there
            will be no change.
        use_mtls (bool): Whether to use mTLS for the request.


    """
    # Only modify the request if mTLS is enabled, and request supports sessions.
    if use_mtls and hasattr(request, "session"):
        # Ensure the request has a session to mount the adapter to.
        if not request.session:
            request.session = requests.Session()

        adapter = _mtls.MdsMtlsAdapter()
        # Mount the adapter for all default GCE metadata hosts.
        for host in _GCE_DEFAULT_MDS_HOSTS:
            request.session.mount(f"https://{host}/", adapter)

