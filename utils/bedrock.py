import os

def bedrock(
    *,
    region: str | None = None,
    base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
    api_key: str | None | NotGiven = NOT_GIVEN,
    token_provider: BedrockTokenProvider | None = None,
    access_key_id: str | None = None,
    secret_access_key: str | None = None,
    session_token: str | None = None,
    profile: str | None = None,
    credential_provider: AwsCredentialsProvider | None = None,
) -> _Provider:
    """Configure the standard OpenAI client for Amazon Bedrock Mantle."""

    normalized_region = _normalize_optional_string(region)
    if region is not None and normalized_region is None:
        raise OpenAIError("The Bedrock AWS `region` must not be empty.")

    region_source: Literal["explicit", "environment"] | None = None
    if normalized_region is not None:
        region_source = "explicit"
    else:
        normalized_region = _normalize_optional_string(
            os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        )
        if normalized_region is not None:
            region_source = "environment"

    configured_base_url: httpx.URL | None
    if isinstance(base_url, NotGiven):
        environment_base_url = _normalize_optional_string(os.environ.get("AWS_BEDROCK_BASE_URL"))
        configured_base_url = _normalize_base_url(environment_base_url) if environment_base_url else None
    elif base_url is None:
        configured_base_url = None
    else:
        if isinstance(base_url, str) and not base_url.strip():
            raise OpenAIError("The Bedrock `base_url` must not be empty.")
        configured_base_url = _normalize_base_url(base_url)

    normalized_profile = _normalize_optional_string(profile)
    if profile is not None and normalized_profile is None:
        raise OpenAIError("The Bedrock AWS `profile` must not be empty.")

    if (access_key_id is None) != (secret_access_key is None) or (session_token is not None and access_key_id is None):
        raise OpenAIError(
            "Static AWS credentials require both `access_key_id` and `secret_access_key`. "
            "A `session_token` may only be used with both."
        )
    if access_key_id is not None and (not access_key_id.strip() or not cast(str, secret_access_key).strip()):
        raise OpenAIError("Static AWS credentials require non-empty `access_key_id` and `secret_access_key` values.")
    if session_token is not None and not session_token.strip():
        raise OpenAIError("A static AWS `session_token` must not be empty when provided.")

    explicit_api_key = not isinstance(api_key, NotGiven) and api_key is not None
    if explicit_api_key and (not isinstance(api_key, str) or not api_key.strip()):
        raise OpenAIError("The Bedrock bearer credential must not be empty.")
    if explicit_api_key and token_provider is not None:
        raise OpenAIError("The `api_key` and `token_provider` options are mutually exclusive. Configure only one.")

    explicit_bearer = explicit_api_key or token_provider is not None
    aws_modes = sum(
        (
            access_key_id is not None,
            normalized_profile is not None,
            credential_provider is not None,
        )
    )
    if aws_modes > 1:
        raise OpenAIError(
            "Bedrock authentication is ambiguous. Configure exactly one explicit AWS mode: static credentials, "
            "profile, or credential provider."
        )
    if explicit_bearer and aws_modes:
        raise OpenAIError(
            "Bedrock authentication is ambiguous. Configure exactly one explicit mode: bearer credential, "
            "static AWS credentials, profile, or credential provider."
        )

    skip_environment_bearer = not isinstance(api_key, NotGiven) and api_key is None
    use_environment_bearer = (
        not explicit_bearer
        and not aws_modes
        and not skip_environment_bearer
        and bool(os.environ.get("AWS_BEARER_TOKEN_BEDROCK"))
    )

    return _create_provider(
        _BedrockProviderDefinition(
            configured_region=normalized_region,
            region_source=region_source,
            configured_base_url=configured_base_url,
            api_key=cast("str | None", api_key) if explicit_api_key else None,
            token_provider=token_provider,
            use_environment_bearer=use_environment_bearer,
            profile=normalized_profile,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            credential_provider=credential_provider,
        )
    )

