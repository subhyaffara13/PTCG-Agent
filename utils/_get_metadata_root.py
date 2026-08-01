
def _get_metadata_root(use_mtls: bool):
    """Returns the metadata server root URL."""

    scheme = "https" if use_mtls else "http"
    return "{}://{}/computeMetadata/v1/".format(scheme, _GCE_METADATA_HOST)

