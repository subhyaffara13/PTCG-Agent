
def get_azure_ad_token_from_username_password(
    client_id: str,
    azure_username: str,
    azure_password: str,
    scope: str = "https://cognitiveservices.azure.com/.default",
) -> Callable[[], str]:
    """
    Get Azure AD token provider from `client_id`, `azure_username`, and `azure_password`

    Args:
        client_id: str
        azure_username: str
        azure_password: str
        scope: str

    Returns:
        callable that returns a bearer token.
    """
    from azure.identity import UsernamePasswordCredential, get_bearer_token_provider

    verbose_logger.debug(
        "client_id=%s, azure_username=[set=%s], azure_password=[set=%s]",
        client_id,
        azure_username is not None,
        azure_password is not None,
    )
    credential = UsernamePasswordCredential(
        client_id=client_id,
        username=azure_username,
        password=azure_password,
    )

    token_provider = get_bearer_token_provider(credential, scope)

    verbose_logger.debug("token_provider %s", token_provider)

    return token_provider

