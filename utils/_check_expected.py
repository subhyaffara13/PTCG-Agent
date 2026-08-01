
def _check_expected(expected):
    def check(ret, func, args):
        if ret:
            return True
        code = ctypes.GetLastError()
        if code == expected:
            return False
        raise ctypes.WinError(code)

    return check

