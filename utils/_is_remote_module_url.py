
def _is_remote_module_url(value: Any) -> bool:
    return isinstance(value, str) and (
        value.startswith("s3://") or value.startswith("gcs://")
    )

