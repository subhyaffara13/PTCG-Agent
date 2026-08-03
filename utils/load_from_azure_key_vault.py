import os

def load_from_azure_key_vault(use_azure_key_vault: bool = False):
    if use_azure_key_vault is False:
        return

    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        # Set your Azure Key Vault URI
        KVUri = os.getenv("AZURE_KEY_VAULT_URI", None)

        if KVUri is None:
            raise Exception(
                "Error when loading keys from Azure Key Vault: AZURE_KEY_VAULT_URI is not set."
            )

        credential = DefaultAzureCredential()

        # Create the SecretClient using the credential
        client = SecretClient(vault_url=KVUri, credential=credential)

        litellm.secret_manager_client = client
        litellm._key_management_system = KeyManagementSystem.AZURE_KEY_VAULT
    except Exception as e:
        _error_str = str(e)
        verbose_proxy_logger.exception(
            "Error when loading keys from Azure Key Vault: %s .Ensure you run `pip install azure-identity azure-keyvault-secrets`",
            _error_str,
        )

