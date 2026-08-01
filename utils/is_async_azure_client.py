
def is_async_azure_client(client: object) -> TypeGuard[AsyncAzureOpenAI]:
    from ..lib.azure import AsyncAzureOpenAI

    return isinstance(client, AsyncAzureOpenAI)

