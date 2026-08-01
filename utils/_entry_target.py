
def _entry_target(entry: object) -> str:
    """Extract the target string from a fingerprint entry."""
    if isinstance(entry, tuple):
        return str(entry[0])
    return str(entry)

