
def _get_domain() -> str:
    """Dynamically determines the domain for IAM credentials based on active mTLS configuration.

    Returns:
        str: The dynamic domain string.
    """
    from google.auth.transport import _mtls_helper

    if (
        hasattr(_mtls_helper, "check_use_client_cert")
        and _mtls_helper.check_use_client_cert()
    ):
        return f"iamcredentials.mtls.{_helpers.DEFAULT_UNIVERSE_DOMAIN}"
    else:
        return f"iamcredentials.{_helpers.DEFAULT_UNIVERSE_DOMAIN}"

