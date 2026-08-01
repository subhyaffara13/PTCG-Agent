
def _is_gcs_url(s: str) -> bool:
    """Check if string is a GCS URL (gs://...)."""
    return isinstance(s, str) and s.startswith("gs://")

