
def _cast_ssl_ctx_to_void_p_stdlib(context):
    return ctypes.c_void_p.from_address(
        id(context) + ctypes.sizeof(ctypes.c_void_p) * 2
    )

