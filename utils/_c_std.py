
def _c_std(stream: str):
    if IS_WINDOWS:
        stream_index = 2 if stream == "stderr" else 1
        try:
            iob_func = libc.__acrt_iob_func
            iob_func.restype = ctypes.POINTER(ctypes.c_void_p)
            iob_func.argtypes = [ctypes.c_uint]
            return iob_func(stream_index)
        except AttributeError:
            pass
        try:
            legacy_index = 2 if stream == "stderr" else 1
            iob = (ctypes.POINTER(ctypes.c_void_p) * 3).in_dll(libc, "_iob")
            return iob[legacy_index]
        except (AttributeError, OSError) as err:
            raise RuntimeError(
                f"Could not resolve C-runtime FILE* for '{stream}'. "
                "Neither __acrt_iob_func nor _iob are available in the loaded CRT."
            ) from err
    return ctypes.c_void_p.in_dll(libc, stream)

