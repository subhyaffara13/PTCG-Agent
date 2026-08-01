
def _get_full_path(proch):
    size = DWORD(MAX_PATH)
    while True:
        path_buff = ctypes.create_unicode_buffer("", size.value)
        if kernel32.QueryFullProcessImageNameW(proch, 0, path_buff, size):
            return path_buff.value
        size.value *= 2

