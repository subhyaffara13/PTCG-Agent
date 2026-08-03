import os

def get_win_folder(csidl_name: str) -> str:
    """Get a Windows folder path, checking for ``WIN_PD_OVERRIDE_*`` environment variable overrides first.

    For example, ``CSIDL_LOCAL_APPDATA`` can be overridden by setting ``WIN_PD_OVERRIDE_LOCAL_APPDATA``.

    """
    env_var = f"WIN_PD_OVERRIDE_{csidl_name.removeprefix('CSIDL_')}"
    if override := os.environ.get(env_var, "").strip():
        return override
    return _resolve_win_folder(csidl_name)

