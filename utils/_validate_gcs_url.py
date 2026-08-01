
def _validate_gcs_url(url: str, label: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(
            f"Mavvrik FOCUS destination: {label} must be HTTPS, got scheme '{parsed.scheme}'"
        )
    hostname = (parsed.hostname or "").lower()
    if not (
        hostname == "storage.googleapis.com"
        or hostname.endswith(".storage.googleapis.com")
    ):
        raise ValueError(
            f"Mavvrik FOCUS destination: {label} must be a GCS endpoint "
            f"(storage.googleapis.com), got '{hostname}'"
        )

