import os
from typing import Optional

def _handle_generic_sso_error(
    e: Exception,
    generic_authorization_endpoint: Optional[str],
    generic_token_endpoint: Optional[str],
    additional_headers: dict,
) -> NoReturn:
    """Handle errors from generic SSO verify_and_process. Always re-raises."""
    error_message = str(e)

    # Surface a helpful PKCE misconfiguration hint only when:
    # 1. The error mentions PKCE/code verifier, AND
    # 2. PKCE is not currently configured (GENERIC_CLIENT_USE_PKCE != true)
    pkce_configured = os.getenv("GENERIC_CLIENT_USE_PKCE", "false").lower() == "true"
    if not pkce_configured and (
        "PKCE" in error_message or "code verifier" in error_message.lower()
    ):
        is_okta = (
            generic_authorization_endpoint
            and "okta" in generic_authorization_endpoint.lower()
        ) or (generic_token_endpoint and "okta" in generic_token_endpoint.lower())
        provider_name = "Okta" if is_okta else "Your OAuth provider"

        detailed_message = (
            f"SSO authentication failed: {provider_name} requires PKCE (Proof Key for Code Exchange) "
            f"but it's not enabled in your LiteLLM configuration.\n\n"
            f"SOLUTION: Add this environment variable and restart your proxy:\n"
            f"  GENERIC_CLIENT_USE_PKCE=true\n\n"
        )
        if is_okta:
            detailed_message += (
                "For AWS ECS: Add the environment variable to your task definition.\n"
                "For Docker: Add -e GENERIC_CLIENT_USE_PKCE=true to your docker run command.\n"
                "For .env file: Add GENERIC_CLIENT_USE_PKCE=true to your .env file.\n\n"
            )
        detailed_message += f"Original error: {error_message}"

        raise ProxyException(
            message=detailed_message,
            type=ProxyErrorTypes.auth_error,
            param="GENERIC_CLIENT_USE_PKCE",
            code=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(e, ProxyException):
        verbose_proxy_logger.error(
            "SSO authentication failed: %s. Passed in headers: %s",
            e,
            additional_headers,
        )
    else:
        verbose_proxy_logger.exception(
            "Error verifying and processing generic SSO: %s. Passed in headers: %s",
            e,
            additional_headers,
        )
    raise e

