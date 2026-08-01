
def _is_console(f: t.TextIO) -> bool:
    if not hasattr(f, "fileno"):
        return False

    try:
        fileno = f.fileno()
    except (OSError, io.UnsupportedOperation):
        return False

    handle = msvcrt.get_osfhandle(fileno)
    return bool(GetConsoleMode(handle, byref(DWORD())))

