
def _provider_for_legacy_client(
    client: BedrockOpenAI | AsyncBedrockOpenAI,
    configuration: _LegacyAuthConfiguration,
) -> _Provider:
    mode, credential = configuration
    if mode == "bearer":
        if not isinstance(credential, str) or not credential:
            raise OpenAIError("The Bedrock bearer credential must not be empty.")
        return bedrock(
            region=client.aws_region,
            base_url=client.base_url,
            api_key=credential,
        )
    if mode == "token_provider":
        return bedrock(
            region=client.aws_region,
            base_url=client.base_url,
            token_provider=cast("AsyncBedrockTokenProvider", credential),
        )

    state = client._bedrock_state
    return bedrock(
        region=client.aws_region,
        base_url=client.base_url,
        profile=state.aws_profile,
        access_key_id=state.aws_access_key_id,
        secret_access_key=state.aws_secret_access_key,
        session_token=state.aws_session_token,
        credential_provider=state.aws_credentials_provider,
    )

