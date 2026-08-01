
def load_offload_lib(offload_lib_path):
    _LOGGER.debug("loading offload library from %s", offload_lib_path)

    # winmode parameter is only available for python 3.8+.
    lib = (
        ctypes.CDLL(offload_lib_path, winmode=0)
        if sys.version_info >= (3, 8) and os.name == "nt"
        else ctypes.CDLL(offload_lib_path)
    )

    # Set up types for:
    # int ConfigureSslContext(SignFunc sign_func, const char *cert, SSL_CTX *ctx)
    lib.ConfigureSslContext.argtypes = [
        SIGN_CALLBACK_CTYPE,
        ctypes.c_char_p,
        ctypes.c_void_p,
    ]
    lib.ConfigureSslContext.restype = ctypes.c_int

    return lib

