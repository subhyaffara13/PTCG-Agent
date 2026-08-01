
def disable_legacy_validation():
    """Disable legacy name validation, instead allowing all UTF8 characters."""
    global _legacy_validation
    _legacy_validation = False

