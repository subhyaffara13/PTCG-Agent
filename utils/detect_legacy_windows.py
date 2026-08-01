
def detect_legacy_windows() -> bool:
    """Detect legacy Windows."""
    return WINDOWS and not get_windows_console_features().vt


def detect_legacy_windows() -> bool:
    """Detect legacy Windows."""
    return WINDOWS and not get_windows_console_features().vt

