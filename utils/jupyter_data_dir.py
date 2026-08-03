import os
import sys
from pathlib import Path


def jupyter_data_dir() -> str:
    """Get the config directory for Jupyter data files for this platform and user.

    These are non-transient, non-configuration files.

    Returns JUPYTER_DATA_DIR if defined, else a platform-appropriate path.
    """
    env = os.environ

    if env.get("JUPYTER_DATA_DIR"):
        return env["JUPYTER_DATA_DIR"]

    if use_platform_dirs():
        return platformdirs.user_data_dir(APPNAME, appauthor=False)

    home = get_home_dir()

    if sys.platform == "darwin":
        return str(Path(home, "Library", "Jupyter"))
    # Bug in mypy which thinks it's unreachable: https://github.com/python/mypy/issues/10773
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", None)
        if appdata:
            return str(Path(appdata, "jupyter").resolve())
        return pjoin(jupyter_config_dir(), "data")
    # Linux, non-OS X Unix, AIX, etc.
    # Bug in mypy which thinks it's unreachable: https://github.com/python/mypy/issues/10773
    xdg = env.get("XDG_DATA_HOME", None)
    if not xdg:
        xdg = pjoin(home, ".local", "share")
    return pjoin(xdg, "jupyter")

