
def is_managed_cloud_storage_uri(file_id: str) -> bool:
    """
    True if file_id is a raw cloud-storage object URI (e.g. ``s3://bucket/key``).

    These are internal provider artifacts. On the multi-tenant proxy they must be
    retrieved through their managed unified file id so owner/team access is enforced;
    a raw URI supplied by a caller bypasses that check.
    """
    return isinstance(file_id, str) and file_id.startswith(
        MANAGED_CLOUD_STORAGE_SCHEMES
    )

