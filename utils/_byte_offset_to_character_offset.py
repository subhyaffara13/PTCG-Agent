
def _byte_offset_to_character_offset(str, offset):
    """Converts a byte based offset in a string to a code-point."""
    as_utf8 = str.encode("utf-8")
    return len(as_utf8[:offset].decode("utf-8", errors="replace"))

