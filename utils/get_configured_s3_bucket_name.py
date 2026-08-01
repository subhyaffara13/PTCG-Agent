
def get_configured_s3_bucket_name(litellm_params: Mapping[str, object]) -> str:
    """
    Resolve the server-configured S3 bucket for Bedrock file operations.

    Only trusts the immutable server-side credential snapshot or the
    environment; never a request-supplied param, since the bucket is what
    `validate_managed_cloud_file_id` checks file ids against.
    """
    trusted_model_credentials = litellm_params.get(
        "_litellm_internal_model_credentials"
    )
    bucket_name: str | None = None
    if isinstance(trusted_model_credentials, MappingProxyType):
        snapshot: dict[str, object] = {}
        snapshot.update(trusted_model_credentials)  # any-ok: untyped snapshot
        bucket_name = _TrustedS3ModelCredentials.model_validate(snapshot).s3_bucket_name
    bucket_name = bucket_name or os.getenv("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError(
            "S3 bucket_name is required. Set 's3_bucket_name' in proxy config or AWS_S3_BUCKET_NAME for Bedrock file content retrieval."
        )
    return bucket_name

