
def _warn_once(msg, category=UserWarning, stacklevel=2):
    if msg not in _WARNINGS_SHOWN:
        _WARNINGS_SHOWN.add(msg)
        warn(msg, category=category, stacklevel=stacklevel)


def _warn_once(
    warning_id: str, message: str, category: type[Warning] = UserWarning
) -> None:
    """Helper to ensure each warning is shown only once per process."""
    if warning_id not in _WARNINGS_SHOWN:
        if not torch.compiler.is_compiling():
            warnings.warn(message, category, stacklevel=2)
        _WARNINGS_SHOWN.add(warning_id)

