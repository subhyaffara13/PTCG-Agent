
def has_magic(s: str | bytes) -> bool:
    if isinstance(s, bytes):
        return magic_check_bytes.search(s) is not None
    else:
        return magic_check.search(s) is not None


def has_magic(s):
    match = magic_check.search(s)
    return match is not None


def has_magic(s):
    match = magic_check.search(s)
    return match is not None

