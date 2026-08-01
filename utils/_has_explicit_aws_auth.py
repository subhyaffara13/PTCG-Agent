
def _has_explicit_aws_auth(
    *,
    aws_profile: str | None,
    aws_access_key_id: str | None,
    aws_secret_access_key: str | None,
    aws_session_token: str | None,
    aws_credentials_provider: AwsCredentialsProvider | None,
) -> bool:
    return any(
        value is not None
        for value in (
            aws_profile,
            aws_access_key_id,
            aws_secret_access_key,
            aws_session_token,
            aws_credentials_provider,
        )
    )

