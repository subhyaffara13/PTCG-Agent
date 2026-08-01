
def _get_cffi_func(func, signature=None):
    # Get function pointer
    func_ptr = ffi.cast('uintptr_t', func)

    # Get signature
    if signature is None:
        signature = ffi.getctype(ffi.typeof(func)).replace('(*)', ' ')

    return func_ptr, signature


def _get_cffi_func(base, signature):
    cffi = pytest.importorskip("cffi")

    # Get function address
    voidp = ctypes.cast(base, ctypes.c_void_p)
    address = voidp.value

    # Create corresponding cffi handle
    ffi = cffi.FFI()
    func = ffi.cast(signature, address)
    return func

