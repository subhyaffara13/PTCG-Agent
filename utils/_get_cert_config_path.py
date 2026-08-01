
def _get_cert_config_path(certificate_config_path=None, include_context_aware=True):
    """Get the certificate configuration path based on the following order:

    1: Explicit override, if set
    2: Environment variable, if set
    3: Well-known location

    Returns "None" if the selected config file does not exist.

    Args:
        certificate_config_path (string): The certificate config path. If provided, the well known
        location and environment variable will be ignored.
        include_context_aware (bool): If context aware metadata path should be checked for the
        SecureConnect mTLS configuration.

    Returns:
        The absolute path of the certificate config file, and None if the file does not exist.
    """

    if certificate_config_path is None:
        env_path = environ.get(environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, None)
        if env_path is not None and env_path != "":
            certificate_config_path = env_path
        else:
            env_path = environ.get(
                environment_vars.CLOUDSDK_CONTEXT_AWARE_CERTIFICATE_CONFIG_FILE_PATH,
                None,
            )
            if include_context_aware and env_path is not None and env_path != "":
                certificate_config_path = env_path
            else:
                certificate_config_path = CERTIFICATE_CONFIGURATION_DEFAULT_PATH

    certificate_config_path = path.expanduser(certificate_config_path)
    if not path.exists(certificate_config_path):
        return None
    return certificate_config_path

