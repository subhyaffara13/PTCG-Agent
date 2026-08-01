
def _get_gce_credentials(request=None, quota_project_id=None):
    """Gets credentials and project ID from the GCE Metadata Service."""
    # While this library is normally bundled with compute_engine, there are
    # some cases where it's not available, so we tolerate ImportError.
    # Compute Engine requires optional `requests` dependency.
    try:
        from google.auth import compute_engine
        from google.auth.compute_engine import _metadata
        import google.auth.transport.requests
    except ImportError:
        _LOGGER.warning("Import of Compute Engine auth library failed.")
        return None, None

    if request is None:
        request = google.auth.transport.requests.Request()

    if _metadata.is_on_gce(request=request):
        # Get the project ID.
        try:
            project_id = _metadata.get_project_id(request=request)
        except exceptions.TransportError:
            project_id = None

        cred = compute_engine.Credentials()
        cred = _apply_quota_project_id(cred, quota_project_id)

        return cred, project_id
    else:
        _LOGGER.warning(
            "Authentication failed using Compute Engine authentication due to unavailable metadata server."
        )
        return None, None


def _get_gce_credentials(request=None):
    """Gets credentials and project ID from the GCE Metadata Service."""
    # Ping requires a transport, but we want application default credentials
    # to require no arguments. So, we'll use the _http_client transport which
    # uses http.client. This is only acceptable because the metadata server
    # doesn't do SSL and never requires proxies.

    # While this library is normally bundled with compute_engine, there are
    # some cases where it's not available, so we tolerate ImportError.

    return _default._get_gce_credentials(request)

