
def check_use_client_cert():
    """Returns boolean for whether the client certificate should be used for mTLS.

    If GOOGLE_API_USE_CLIENT_CERTIFICATE is set to true or false, a corresponding
    bool value will be returned. If the value is set to an unexpected string, it
    will default to False.
    If GOOGLE_API_USE_CLIENT_CERTIFICATE is unset, the value will be inferred
    by reading a file pointed at by GOOGLE_API_CERTIFICATE_CONFIG, and verifying
    it contains a "workload" section. If so, the function will return True,
    otherwise False.

    Returns:
        bool: Whether the client certificate should be used for mTLS connection.
    """
    use_client_cert = getenv(environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE)
    if use_client_cert is None or use_client_cert == "":
        use_client_cert = getenv(
            environment_vars.CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE
        )

    # Check if the value of GOOGLE_API_USE_CLIENT_CERTIFICATE is set.
    if use_client_cert:
        return use_client_cert.lower() == "true"
    else:
        # Check if the value of GOOGLE_API_CERTIFICATE_CONFIG is set.
        cert_path = getenv(environment_vars.GOOGLE_API_CERTIFICATE_CONFIG)
        if cert_path is None:
            cert_path = getenv(
                environment_vars.CLOUDSDK_CONTEXT_AWARE_CERTIFICATE_CONFIG_FILE_PATH
            )

        if cert_path:
            try:
                with open(cert_path, "r") as f:
                    content = json.load(f)
                    # verify json has workload key
                    content["cert_configs"]["workload"]
                    return True
            except (
                FileNotFoundError,
                OSError,
                KeyError,
                TypeError,
                json.JSONDecodeError,
            ) as e:
                _LOGGER.debug("error decoding certificate: %s", e)
        return False

