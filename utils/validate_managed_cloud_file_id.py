from typing import Tuple

def validate_managed_cloud_file_id(
    file_id: str,
    scheme: str,
    configured_bucket_name: str,
    allowed_object_prefixes: Sequence[str],
    allow_legacy_cloud_file_ids: bool = False,
) -> Tuple[str, str]:
    decoded_file_id = unquote(file_id)
    if not decoded_file_id.startswith(scheme):
        raise ValueError(f"file_id must be a {scheme} URI")

    full_path = decoded_file_id[len(scheme) :]
    if "/" not in full_path:
        raise ValueError("file_id must include a cloud storage object name")

    bucket_name, object_name = full_path.split("/", 1)
    configured_bucket, configured_prefix = split_configured_cloud_bucket_name(
        configured_bucket_name
    )
    if bucket_name != configured_bucket:
        raise ValueError("file_id bucket does not match the configured storage bucket")

    _validate_cloud_object_path(object_name)
    allowed_prefixes = tuple(allowed_object_prefixes)
    if configured_prefix:
        allowed_prefixes = tuple(
            f"{configured_prefix.rstrip('/')}/{prefix}" for prefix in allowed_prefixes
        )

    if object_name.startswith(allowed_prefixes):
        return bucket_name, object_name

    if allow_legacy_cloud_file_ids:
        if configured_prefix and not object_name.startswith(
            f"{configured_prefix.rstrip('/')}/"
        ):
            raise ValueError(
                "file_id object does not match the configured storage prefix"
            )
        return bucket_name, object_name

    raise ValueError("file_id must reference a LiteLLM-managed storage object")

