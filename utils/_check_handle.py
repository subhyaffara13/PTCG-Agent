
def _check_handle(error_val=0):
    def check(ret, func, args):
        if ret == error_val:
            raise ctypes.WinError()
        return ret

    return check

