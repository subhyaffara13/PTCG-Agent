
def _get_metadata_ip_root(use_mtls: bool):
    """Returns the metadata server IP root URL."""
    scheme = "https" if use_mtls else "http"
    return "{}://{}".format(
        scheme, os.getenv(environment_vars.GCE_METADATA_IP, _GCE_DEFAULT_MDS_IP)
    )

