
def has_default_client_cert_source(include_context_aware=True):
    """Check if default client SSL credentials exists on the device.

    Args:
       include_context_aware (bool): include_context_aware indicates if context_aware
       path location will be checked or should it be skipped.

    Returns:
        bool: indicating if the default client cert source exists.
    """
    if (
        include_context_aware
        and _mtls_helper._check_config_path(_mtls_helper.CONTEXT_AWARE_METADATA_PATH)
        is not None
    ):
        return True
    if (
        _mtls_helper._check_config_path(
            _mtls_helper.CERTIFICATE_CONFIGURATION_DEFAULT_PATH
        )
        is not None
    ):
        return True
    cert_config_path = getenv("GOOGLE_API_CERTIFICATE_CONFIG")
    if (
        cert_config_path
        and _mtls_helper._check_config_path(cert_config_path) is not None
    ):
        return True
    return False

