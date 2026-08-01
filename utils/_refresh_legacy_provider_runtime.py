
def _refresh_legacy_provider_runtime(client: BedrockOpenAI | AsyncBedrockOpenAI) -> None:
    _synchronize_legacy_routing_state(client)
    configuration = client._legacy_auth_configuration()
    signature = _legacy_runtime_signature(client, configuration)
    if signature == client._bedrock_runtime_signature:
        return

    provider = _provider_for_legacy_client(client, configuration)
    client._bedrock_provider = provider
    client._provider = provider
    client._provider_runtime = _configure_provider(provider)
    if (
        isinstance(client._provider_runtime, _BedrockProviderRuntime)
        and client.aws_region is None
        and client._provider_runtime.region is not None
    ):
        client.aws_region = client._provider_runtime.region
        client._bedrock_state = replace(client._bedrock_state, aws_region=client.aws_region)
    client._bedrock_runtime_signature = _legacy_runtime_signature(client, configuration)

