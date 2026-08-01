
def should_use_mds_mtls(mds_mtls_config: MdsMtlsConfig = MdsMtlsConfig()):
    """Determines if mTLS should be used for the metadata server."""
    mode = _parse_mds_mode()
    if mode == MdsMtlsMode.STRICT:
        if not _certs_exist(mds_mtls_config):
            raise exceptions.MutualTLSChannelError(
                "mTLS certificates not found in strict mode."
            )
        return True
    elif mode == MdsMtlsMode.NONE:
        return False
    else:  # Default mode
        return _certs_exist(mds_mtls_config)

