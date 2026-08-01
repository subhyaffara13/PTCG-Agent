
def _cast_ssl_ctx_to_void_p_pyopenssl(ssl_ctx):
    return ctypes.cast(int(cffi.FFI().cast("intptr_t", ssl_ctx)), ctypes.c_void_p)

