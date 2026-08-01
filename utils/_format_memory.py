
def _format_memory(nbytes):
    """Return a formatted memory size string."""
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    if abs(nbytes) >= GB:
        return f"{nbytes * 1.0 / GB:.2f} GB"
    elif abs(nbytes) >= MB:
        return f"{nbytes * 1.0 / MB:.2f} MB"
    elif abs(nbytes) >= KB:
        return f"{nbytes * 1.0 / KB:.2f} KB"
    else:
        return str(nbytes) + " B"

