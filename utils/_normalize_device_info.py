
def _normalize_device_info(device_type: str, device_id: int) -> str:
    """Device info normalization."""
    if device_type == "cpu":
        return "cpu"
    return f"{device_type}:{device_id}"

