
def get_ssl_verify(
    ssl_verify: Optional[Union[bool, str]] = None,
) -> Union[bool, str]:
    """
    Common utility to resolve the SSL verification setting.
    Prioritizes:
    1. Passed-in ssl_verify
    2. os.environ["SSL_VERIFY"]
    3. litellm.ssl_verify
    4. os.environ["SSL_CERT_FILE"] (if ssl_verify is True)

    Returns:
        Union[bool, str]: The resolved SSL verification setting (bool or path to CA bundle)
    """
    from litellm.secret_managers.main import str_to_bool

    if ssl_verify is None:
        ssl_verify = os.getenv("SSL_VERIFY", litellm.ssl_verify)

    # Convert string "False"/"True" to boolean if applicable
    if isinstance(ssl_verify, str):
        # If it's a file path, return it directly
        if os.path.exists(ssl_verify):
            return ssl_verify

        # Otherwise, check if it's a boolean string
        ssl_verify_bool = str_to_bool(ssl_verify)
        if ssl_verify_bool is not None:
            ssl_verify = ssl_verify_bool

    # If SSL verification is enabled, check for SSL_CERT_FILE override
    if ssl_verify is True:
        ssl_cert_file = os.getenv("SSL_CERT_FILE")
        if ssl_cert_file and os.path.exists(ssl_cert_file):
            return ssl_cert_file

    return ssl_verify if ssl_verify is not None else True

