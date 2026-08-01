
def _pick_get_win_folder() -> Callable[[str], str]:
    """Select the best method to resolve Windows folder paths: ctypes, then registry, then environment variables."""
    try:
        import ctypes  # noqa: PLC0415, F401
    except ImportError:
        pass
    else:
        return get_win_folder_via_ctypes
    try:
        import winreg  # noqa: PLC0415, F401
    except ImportError:
        return get_win_folder_from_env_vars
    else:
        return get_win_folder_from_registry


def _pick_get_win_folder() -> Callable[[str], str]:
    try:
        import ctypes  # noqa: PLC0415
    except ImportError:
        pass
    else:
        if hasattr(ctypes, "windll"):
            return get_win_folder_via_ctypes
    try:
        import winreg  # noqa: PLC0415, F401
    except ImportError:
        return get_win_folder_from_env_vars
    else:
        return get_win_folder_from_registry


def _pick_get_win_folder() -> Callable[[str], str]:
    try:
        import ctypes  # noqa: PLC0415
    except ImportError:
        pass
    else:
        if hasattr(ctypes, "windll"):
            return get_win_folder_via_ctypes
    try:
        import winreg  # noqa: PLC0415, F401
    except ImportError:
        return get_win_folder_from_env_vars
    else:
        return get_win_folder_from_registry

