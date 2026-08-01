
def get_windows_console_features() -> "WindowsConsoleFeatures":  # pragma: no cover
    global _windows_console_features
    if _windows_console_features is not None:
        return _windows_console_features
    from ._windows import get_windows_console_features

    _windows_console_features = get_windows_console_features()
    return _windows_console_features


def get_windows_console_features() -> "WindowsConsoleFeatures":  # pragma: no cover
    global _windows_console_features
    if _windows_console_features is not None:
        return _windows_console_features
    from ._windows import get_windows_console_features

    _windows_console_features = get_windows_console_features()
    return _windows_console_features

