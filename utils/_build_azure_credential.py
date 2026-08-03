import os
from typing import Optional

def _build_azure_credential(
    azure_client_id: Optional[str] = None,
    azure_tenant_id: Optional[str] = None,
    azure_client_secret: Optional[str] = None,
):
    """
    Build a long-lived Azure credential object.

    Azure SDK credentials cache tokens internally and handle expiry/refresh
    transparently, so this should be called once and the result reused.
    """
    try:
        from azure.identity import (
            ClientSecretCredential,
            DefaultAzureCredential,
            ManagedIdentityCredential,
        )
    except ImportError:
        raise ImportError(
            "azure-identity is required for Azure AD Redis authentication. "
            "Install it with: pip install azure-identity"
        )

    _client_id = azure_client_id or os.environ.get("AZURE_CLIENT_ID")
    _tenant_id = azure_tenant_id or os.environ.get("AZURE_TENANT_ID")
    _client_secret = azure_client_secret or os.environ.get("AZURE_CLIENT_SECRET")

    if _client_id and _tenant_id and _client_secret:
        return ClientSecretCredential(
            client_id=_client_id,
            tenant_id=_tenant_id,
            client_secret=_client_secret,
        )
    elif _client_id:
        return ManagedIdentityCredential(client_id=_client_id)
    else:
        return DefaultAzureCredential()

