
def _format_base64_size(num_chars: int) -> str:
    """Return a human-readable byte-size estimate from a base64 character count."""
    num_bytes = num_chars * 3 / 4
    if num_bytes >= _BYTES_PER_MIB:
        return f"{num_bytes / _BYTES_PER_MIB:.2f}MB"
    if num_bytes >= _BYTES_PER_KIB:
        return f"{num_bytes / _BYTES_PER_KIB:.1f}KB"
    return f"{int(num_bytes)}B"

