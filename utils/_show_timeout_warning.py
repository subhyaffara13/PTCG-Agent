
def _show_timeout_warning() -> None:
    global _SHOWN_TIMEOUT_WARNING
    if not _SHOWN_TIMEOUT_WARNING:
        _SHOWN_TIMEOUT_WARNING = True
        message = "Warning: Timeout is not available on main browser thread"
        js.console.warn(message)


def _show_timeout_warning() -> None:
    global _SHOWN_TIMEOUT_WARNING
    if not _SHOWN_TIMEOUT_WARNING:
        _SHOWN_TIMEOUT_WARNING = True
        message = "Warning: Timeout is not available on main browser thread"
        js.console.warn(message)

