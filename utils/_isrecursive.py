
def _isrecursive(pattern: str | bytes) -> bool:
    if isinstance(pattern, bytes):
        return pattern == b'**'
    else:
        return pattern == '**'

