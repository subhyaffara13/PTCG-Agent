
def split_configured_cloud_bucket_name(bucket_name: str) -> Tuple[str, str]:
    if not isinstance(bucket_name, str) or not bucket_name.strip():
        raise ValueError("Cloud storage bucket name is required")

    bucket_name = bucket_name.strip()
    if "://" in bucket_name or "?" in bucket_name or "#" in bucket_name:
        raise ValueError(
            "Cloud storage bucket name must not include a URI scheme or query"
        )
    if any(ord(char) < 32 or ord(char) == 127 for char in bucket_name):
        raise ValueError("Cloud storage bucket name contains control characters")

    bucket, _, prefix = bucket_name.partition("/")
    if not bucket:
        raise ValueError("Cloud storage bucket name is required")
    if "\\" in bucket:
        raise ValueError("Cloud storage bucket name contains an invalid separator")

    prefix = prefix.strip("/")
    if prefix:
        _validate_cloud_object_path(prefix)

    return bucket, prefix

