
def _isUncanonicalNumber(s):
    f = float(s)
    if f not in _CANONICAL_NUMBERS:
        return False  # Only the canonical numbers are required to be canonical.
    return s != floatToGoString(f)

