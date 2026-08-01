
def _copy_configuration(
    client: BedrockOpenAI | AsyncBedrockOpenAI,
    *,
    api_key: str | None,
    token_provider: BedrockTokenProvider | AsyncBedrockTokenProvider | None,
    aws_region: str | None,
    aws_profile: str | None,
    aws_access_key_id: str | None,
    aws_secret_access_key: str | None,
    aws_session_token: str | None,
    aws_credentials_provider: AwsCredentialsProvider | None,
    base_url: str | httpx.URL | None,
) -> tuple[dict[str, object], _Provider | None, _LegacyBedrockState | None]:
    _synchronize_legacy_routing_state(client)
    state = client._bedrock_state
    current_api_key = client.api_key or ""
    api_key_was_mutated = state.token_provider is None and current_api_key != _state_api_key(state)
    aws_override = _has_explicit_aws_auth(
        aws_profile=aws_profile,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        aws_credentials_provider=aws_credentials_provider,
    )
    explicit_bearer_override = api_key is not None or token_provider is not None
    if explicit_bearer_override and aws_override:
        raise OpenAIError(
            "Bedrock authentication is ambiguous. Configure exactly one explicit mode: bearer credential, "
            "static AWS credentials, profile, or credential provider."
        )

    effective_api_key = (
        api_key
        if api_key is not None
        else current_api_key
        if api_key_was_mutated and token_provider is None and not aws_override
        else None
    )
    bearer_override = effective_api_key is not None or token_provider is not None

    routing_override = aws_region is not None or base_url is not None
    if not bearer_override and not aws_override and not routing_override:
        _refresh_legacy_provider_runtime(client)
        return {}, client._bedrock_provider, client._bedrock_state

    if bearer_override:
        next_api_key = effective_api_key
        next_token_provider = token_provider
        next_profile = None
        next_access_key_id = None
        next_secret_access_key = None
        next_session_token = None
        next_credentials_provider = None
    elif aws_override:
        next_api_key = None
        next_token_provider = None
        next_profile = aws_profile
        next_access_key_id = aws_access_key_id
        next_secret_access_key = aws_secret_access_key
        next_session_token = aws_session_token
        next_credentials_provider = aws_credentials_provider
    else:
        next_api_key = state.explicit_api_key
        next_token_provider = state.token_provider
        if state.uses_environment_bearer:
            next_api_key = state.environment_bearer_token or _environment_bearer_token()
            next_token_provider = None
        next_profile = state.aws_profile
        next_access_key_id = state.aws_access_key_id
        next_secret_access_key = state.aws_secret_access_key
        next_session_token = state.aws_session_token
        next_credentials_provider = state.aws_credentials_provider

    next_region = aws_region if aws_region is not None else client.aws_region
    next_region_was_explicit = aws_region is not None or state.region_was_explicit
    if aws_profile is not None and aws_region is None and not state.region_was_explicit:
        next_region = None

    if base_url is not None:
        next_base_url: str | httpx.URL | None = base_url
    elif state.uses_region_derived_base_url:
        next_base_url = ""
    else:
        next_base_url = client.base_url

    provider_kwargs: dict[str, object] = {
        "api_key": next_api_key,
        "bedrock_token_provider": next_token_provider,
        "aws_region": next_region,
        "aws_profile": next_profile,
        "aws_access_key_id": next_access_key_id,
        "aws_secret_access_key": next_secret_access_key,
        "aws_session_token": next_session_token,
        "aws_credentials_provider": next_credentials_provider,
        "base_url": next_base_url,
    }
    if _constructor_accepts_keyword(client.__class__.__init__, "_region_was_explicit"):
        provider_kwargs["_region_was_explicit"] = next_region_was_explicit

    return provider_kwargs, None, None

