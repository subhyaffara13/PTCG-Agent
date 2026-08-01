
def should_use_client_cert():
    """Returns boolean for whether the client certificate should be used for mTLS.

    This is a wrapper around _mtls_helper.check_use_client_cert().
    If GOOGLE_API_USE_CLIENT_CERTIFICATE is set to true or false, a corresponding
    bool value will be returned
    If GOOGLE_API_USE_CLIENT_CERTIFICATE is unset, the value will be inferred by
    reading a file pointed at by GOOGLE_API_CERTIFICATE_CONFIG, and verifying it
    contains a "workload" section. If so, the function will return True,
    otherwise False.

    Returns:
       bool: indicating whether the client certificate should be used for mTLS.
    """
    return _mtls_helper.check_use_client_cert()

