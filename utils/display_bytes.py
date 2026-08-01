
def display_bytes(b: int, unit: str = "MiB") -> str:
    """
    return a string that represent the number of bytes in a desired unit
    """
    if unit == "KiB":
        return f"{b / 2**10:.2f} KiB"
    if unit == "MiB":
        return f"{b / 2**20:.2f} MiB"
    if unit == "GiB":
        return f"{b / 2**30:.2f} GiB"
    return f"{b:.2f} bytes"

