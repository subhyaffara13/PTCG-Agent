import os

def _parse_mds_mode():
    """Parses the GCE_METADATA_MTLS_MODE environment variable."""
    mode_str = os.environ.get(environment_vars.GCE_METADATA_MTLS_MODE, "none").lower()
    try:
        return MdsMtlsMode(mode_str)
    except ValueError:
        raise ValueError(
            "Invalid value for GCE_METADATA_MTLS_MODE. Must be one of 'strict', 'none', or 'default'."
        )

