
def _get_workload_cert_and_key_paths(config_path, include_context_aware=True):
    absolute_path = _get_cert_config_path(config_path, include_context_aware)
    if absolute_path is None:
        return None, None

    data = _load_json_file(absolute_path)

    if "cert_configs" not in data:
        raise exceptions.ClientCertError(
            'Certificate config file {} is in an invalid format, a "cert configs" object is expected'.format(
                absolute_path
            )
        )
    cert_configs = data["cert_configs"]

    # We return None, None if the expected workload fields are not present.
    # The certificate config might be present for other types of connections (e.g. gECC),
    # and we want to gracefully fallback to testing other mTLS configurations
    # like SecureConnect instead of throwing an exception.

    if "workload" not in cert_configs:
        return None, None
    workload = cert_configs["workload"]

    if "cert_path" not in workload:
        return None, None
    cert_path = workload["cert_path"]

    if "key_path" not in workload:
        return None, None
    key_path = workload["key_path"]

    # == BEGIN Temporary Cloud Run PATCH ==
    # See https://github.com/googleapis/google-auth-library-python/issues/1881
    if (cert_path == _INCORRECT_CLOUD_RUN_CERT_PATH) and (
        key_path == _INCORRECT_CLOUD_RUN_KEY_PATH
    ):
        if not path.exists(cert_path) and not path.exists(key_path):
            _LOGGER.debug(
                "Applying Cloud Run certificate path patch. "
                "Configured paths not found: %s, %s. "
                "Using well-known paths: %s, %s",
                cert_path,
                key_path,
                _WELL_KNOWN_CLOUD_RUN_CERT_PATH,
                _WELL_KNOWN_CLOUD_RUN_KEY_PATH,
            )
            cert_path = _WELL_KNOWN_CLOUD_RUN_CERT_PATH
            key_path = _WELL_KNOWN_CLOUD_RUN_KEY_PATH
    # == END Temporary Cloud Run PATCH ==

    return cert_path, key_path

