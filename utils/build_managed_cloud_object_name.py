
def build_managed_cloud_object_name(
    prefix: str, filename: Optional[str], fallback_filename: str = "file"
) -> str:
    safe_filename = sanitize_cloud_object_component(
        filename, fallback=fallback_filename
    )
    return f"{prefix}{uuid.uuid4().hex}-{safe_filename}"

