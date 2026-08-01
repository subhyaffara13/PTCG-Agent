
def _synchronize_legacy_routing_state(client: BedrockOpenAI | AsyncBedrockOpenAI) -> None:
    previous_signature = client._bedrock_runtime_signature
    base_url_changed = str(client.base_url) != previous_signature.base_url
    region_changed = client.aws_region != previous_signature.region
    if base_url_changed:
        client._bedrock_state = replace(client._bedrock_state, uses_region_derived_base_url=False)
        client._uses_region_derived_base_url = False
    if region_changed:
        client._bedrock_state = replace(
            client._bedrock_state,
            aws_region=client.aws_region,
            region_was_explicit=client.aws_region is not None,
        )
        if client._bedrock_state.uses_region_derived_base_url and client.aws_region is not None:
            client.base_url = f"https://bedrock-mantle.{client.aws_region}.api.aws/openai/v1"

