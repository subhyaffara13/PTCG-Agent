import os

def _legacy_provider(
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
    region_was_explicit: bool | None = None,
) -> tuple[_Provider, _LegacyBedrockState, str]:
    if callable(cast(object, api_key)):
        raise OpenAIError("Pass refreshable Bedrock credentials via `bedrock_token_provider`, not `api_key`.")
    if api_key == "":
        raise OpenAIError("The `api_key` argument must not be empty.")
    if api_key is not None and token_provider is not None:
        raise OpenAIError(
            "Bedrock authentication is ambiguous. Configure exactly one explicit mode: bearer credential, "
            "static AWS credentials, profile, or credential provider."
        )

    explicit_aws_auth = _has_explicit_aws_auth(
        aws_profile=aws_profile,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        aws_credentials_provider=aws_credentials_provider,
    )
    if (api_key is not None or token_provider is not None) and explicit_aws_auth:
        raise OpenAIError(
            "Bedrock authentication is ambiguous. Configure exactly one explicit mode: bearer credential, "
            "static AWS credentials, profile, or credential provider."
        )

    environment_token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
    uses_environment_bearer = (
        api_key is None and token_provider is None and not explicit_aws_auth and bool(environment_token)
    )
    resolved_region = _configured_region(aws_region)
    uses_region_derived_base_url = _uses_region_derived_base_url(base_url)

    provider_base_url: str | httpx.URL | None | NotGiven
    if isinstance(base_url, str) and not base_url.strip():
        provider_base_url = None
    elif base_url is None:
        provider_base_url = NOT_GIVEN
    else:
        provider_base_url = base_url

    provider = bedrock(
        region=aws_region,
        base_url=provider_base_url,
        api_key=api_key if api_key is not None else environment_token if uses_environment_bearer else NOT_GIVEN,
        token_provider=token_provider,
        access_key_id=aws_access_key_id,
        secret_access_key=aws_secret_access_key,
        session_token=aws_session_token,
        profile=aws_profile,
        credential_provider=aws_credentials_provider,
    )
    state = _LegacyBedrockState(
        explicit_api_key=api_key,
        token_provider=token_provider,
        aws_region=resolved_region,
        region_was_explicit=(
            bool(aws_region and aws_region.strip()) if region_was_explicit is None else region_was_explicit
        ),
        aws_profile=aws_profile,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        aws_credentials_provider=aws_credentials_provider,
        uses_environment_bearer=uses_environment_bearer,
        environment_bearer_token=environment_token if uses_environment_bearer else None,
        uses_region_derived_base_url=uses_region_derived_base_url,
    )
    return provider, state, api_key or (environment_token if uses_environment_bearer else "") or ""

