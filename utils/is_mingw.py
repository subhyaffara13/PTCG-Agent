import sys

def is_mingw() -> bool:
    """Returns True if the current platform is mingw.

    Python compiled with Mingw-w64 has sys.platform == 'win32' and
    get_platform() starts with 'mingw'.
    """
    return sys.platform == 'win32' and get_platform().startswith('mingw')

