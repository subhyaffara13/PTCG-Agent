
def get_raw_stream_name(device_idx: int) -> str:
    """Generate variable name for a raw stream handle on the given device."""
    return f"raw_stream{device_idx}"

