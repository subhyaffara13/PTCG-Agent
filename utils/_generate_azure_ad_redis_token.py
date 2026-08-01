
def _generate_azure_ad_redis_token(
    azure_client_id: Optional[str] = None,
    azure_tenant_id: Optional[str] = None,
    azure_client_secret: Optional[str] = None,
) -> str:
    """
    One-shot helper that builds a credential and fetches a single Azure AD
    access token for Redis. Each call rebuilds the credential and performs a
    network round-trip, so it should not be used in steady-state Redis flows
    — the sync (``create_azure_ad_redis_connect_func``) and async paths
    (``AzureADCredentialProvider``) keep the credential alive across
    connections so the Azure SDK's internal cache + silent refresh apply.
    """
    credential = _build_azure_credential(
        azure_client_id=azure_client_id,
        azure_tenant_id=azure_tenant_id,
        azure_client_secret=azure_client_secret,
    )
    token = credential.get_token(AZURE_REDIS_SCOPE)
    return token.token

