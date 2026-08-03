import json
import os
from typing import Optional

def get_azure_ad_token_from_oidc(
    azure_ad_token: str,
    azure_client_id: Optional[str] = None,
    azure_tenant_id: Optional[str] = None,
    scope: Optional[str] = None,
) -> str:
    """
    Get Azure AD token from OIDC token

    Args:
        azure_ad_token: str
        azure_client_id: Optional[str]
        azure_tenant_id: Optional[str]
        scope: str

    Returns:
        `azure_ad_token_access_token` - str
    """
    if scope is None:
        scope = "https://cognitiveservices.azure.com/.default"
    azure_authority_host = os.getenv(
        "AZURE_AUTHORITY_HOST", "https://login.microsoftonline.com"
    )
    azure_client_id = azure_client_id or os.getenv("AZURE_CLIENT_ID")
    azure_tenant_id = azure_tenant_id or os.getenv("AZURE_TENANT_ID")
    if azure_client_id is None or azure_tenant_id is None:
        raise AzureOpenAIError(
            status_code=422,
            message="AZURE_CLIENT_ID and AZURE_TENANT_ID must be set",
        )

    oidc_token = get_secret_str(azure_ad_token)

    if oidc_token is None:
        raise AzureOpenAIError(
            status_code=401,
            message="OIDC token could not be retrieved from secret manager.",
        )

    azure_ad_token_cache_key = json.dumps(
        {
            "azure_client_id": azure_client_id,
            "azure_tenant_id": azure_tenant_id,
            "azure_authority_host": azure_authority_host,
            "oidc_token": oidc_token,
        }
    )

    azure_ad_token_access_token = azure_ad_cache.get_cache(azure_ad_token_cache_key)
    if azure_ad_token_access_token is not None:
        return azure_ad_token_access_token

    client = litellm.module_level_client

    req_token = client.post(
        f"{azure_authority_host}/{azure_tenant_id}/oauth2/v2.0/token",
        data={
            "client_id": azure_client_id,
            "grant_type": "client_credentials",
            "scope": scope,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": oidc_token,
        },
    )

    if req_token.status_code != 200:
        raise AzureOpenAIError(
            status_code=req_token.status_code,
            message=req_token.text,
        )

    azure_ad_token_json = req_token.json()
    azure_ad_token_access_token = azure_ad_token_json.get("access_token", None)
    azure_ad_token_expires_in = azure_ad_token_json.get("expires_in", None)

    if azure_ad_token_access_token is None:
        raise AzureOpenAIError(
            status_code=422, message="Azure AD Token access_token not returned"
        )

    if azure_ad_token_expires_in is None:
        raise AzureOpenAIError(
            status_code=422, message="Azure AD Token expires_in not returned"
        )

    azure_ad_cache.set_cache(
        key=azure_ad_token_cache_key,
        value=azure_ad_token_access_token,
        ttl=azure_ad_token_expires_in,
    )

    return azure_ad_token_access_token

