
def get_libc():
    if IS_MACOS:
        logger.warning("NOTE: Redirects are currently not supported in MacOs.")
        return None
    elif IS_WINDOWS:
        for lib_name in ("ucrtbase", "msvcrt", "msvcr110", "msvcr100"):
            try:
                lib = ctypes.CDLL(lib_name)
                logger.debug("Loaded Windows C runtime: %s", lib_name)
                return lib
            except OSError:
                continue
        raise RuntimeError(
            "Could not load a C runtime DLL on Windows (tried: ucrtbase, msvcrt, "
            "msvcr110, msvcr100). Redirects cannot function without a CRT."
        )
    else:
        return ctypes.CDLL("libc.so.6")

