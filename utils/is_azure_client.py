
def is_azure_client(client: object) -> TypeGuard[AzureOpenAI]:
    from ..lib.azure import AzureOpenAI

    return isinstance(client, AzureOpenAI)

