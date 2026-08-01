
def _image_url_payload_may_need_sync_gcs_metadata_fetch(
    raw_image_url: Any,
) -> bool:
    """
    True when this image_url value (content-part image_url or assistant ``images[]``
    entry) can trigger a blocking GCS metadata read for MIME resolution.
    """
    fmt: Optional[str] = None
    url: Optional[str] = None
    if isinstance(raw_image_url, dict):
        url = raw_image_url.get("url")  # type: ignore[assignment]
        if not isinstance(url, str):
            return False
        fmt = (
            raw_image_url.get("format")
            or raw_image_url.get("mime_type")
            or raw_image_url.get("content_type")
        )
    elif isinstance(raw_image_url, str):
        url = raw_image_url
    else:
        return False
    if "gs://" not in url or fmt:
        return False
    return _gs_uri_requires_content_type_metadata(url)

