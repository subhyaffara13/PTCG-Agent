
def is_canonical_ipv4_address(host: str) -> bool:
    """Check if host is a canonical dotted-quad IPv4 address.

    Rejects the legacy numeric forms that ``socket`` still accepts and
    maps onto an address, e.g. ``2130706433``, ``017700000001``, ``127.1``.
    """
    parts = host.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        # Each octet must be 1-3 ASCII digits; reject unicode digits
        # (which ``str.isdigit`` accepts but ``int`` may not), octal
        # leading zeros, and values above 255.
        if not (1 <= len(part) <= 3) or not part.isascii() or not part.isdigit():
            return False
        if part[0] == "0" and len(part) != 1:
            return False
        if int(part) > 255:
            return False
    return True

