
def _setup_generic_sso_env_vars(
    generic_client_id: str, redirect_url: str
) -> Tuple[str, List[str], str, str, str, bool]:
    """Setup and validate Generic SSO environment variables."""
    generic_client_secret = os.getenv("GENERIC_CLIENT_SECRET", None)
    generic_scope = os.getenv("GENERIC_SCOPE", "openid email profile").split(" ")
    generic_authorization_endpoint = os.getenv("GENERIC_AUTHORIZATION_ENDPOINT", None)
    generic_token_endpoint = os.getenv("GENERIC_TOKEN_ENDPOINT", None)
    generic_userinfo_endpoint = os.getenv("GENERIC_USERINFO_ENDPOINT", None)
    generic_include_client_id = (
        os.getenv("GENERIC_INCLUDE_CLIENT_ID", "false").lower() == "true"
    )

    # Validate required environment variables
    if generic_client_secret is None:
        raise ProxyException(
            message="GENERIC_CLIENT_SECRET not set. Set it in .env file",
            type=ProxyErrorTypes.auth_error,
            param="GENERIC_CLIENT_SECRET",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if generic_authorization_endpoint is None:
        raise ProxyException(
            message="GENERIC_AUTHORIZATION_ENDPOINT not set. Set it in .env file",
            type=ProxyErrorTypes.auth_error,
            param="GENERIC_AUTHORIZATION_ENDPOINT",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if generic_token_endpoint is None:
        raise ProxyException(
            message="GENERIC_TOKEN_ENDPOINT not set. Set it in .env file",
            type=ProxyErrorTypes.auth_error,
            param="GENERIC_TOKEN_ENDPOINT",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if generic_userinfo_endpoint is None:
        raise ProxyException(
            message="GENERIC_USERINFO_ENDPOINT not set. Set it in .env file",
            type=ProxyErrorTypes.auth_error,
            param="GENERIC_USERINFO_ENDPOINT",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    verbose_proxy_logger.debug(
        f"authorization_endpoint: {generic_authorization_endpoint}\ntoken_endpoint: {generic_token_endpoint}\nuserinfo_endpoint: {generic_userinfo_endpoint}"
    )
    verbose_proxy_logger.debug(
        f"GENERIC_REDIRECT_URI: {redirect_url}\nGENERIC_CLIENT_ID: {generic_client_id}\n"
    )

    return (
        generic_client_secret,
        generic_scope,
        generic_authorization_endpoint,
        generic_token_endpoint,
        generic_userinfo_endpoint,
        generic_include_client_id,
    )

