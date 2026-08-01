
def _validate_gce_mds_configured_environment():
    """Validates the GCE metadata server environment configuration for mTLS.

    mTLS is only supported when connecting to the default metadata server hosts.
    If we are in strict mode (which requires mTLS), ensure that the metadata host
    has not been overridden to a custom value (which means mTLS will fail).

    Raises:
        google.auth.exceptions.MutualTLSChannelError: if the environment
            configuration is invalid for mTLS.
    """
    mode = _mtls._parse_mds_mode()
    if mode == _mtls.MdsMtlsMode.STRICT:
        # mTLS is only supported when connecting to the default metadata host.
        # Raise an exception if we are in strict mode (which requires mTLS)
        # but the metadata host has been overridden to a custom MDS. (which means mTLS will fail)
        if _GCE_METADATA_HOST not in _GCE_DEFAULT_MDS_HOSTS:
            raise exceptions.MutualTLSChannelError(
                "Mutual TLS is required, but the metadata host has been overridden. "
                "mTLS is only supported when connecting to the default metadata host."
            )

