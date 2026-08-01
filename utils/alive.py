
def alive(pid: int) -> bool:
    """Is the process alive?"""
    if sys.platform == "win32":
        # why can't anything be easy...
        status = DWORD()
        handle = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
        GetExitCodeProcess(handle, ctypes.byref(status))
        return status.value == 259  # STILL_ACTIVE
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

