
def _get_cffi_data(data):
    # Get pointer
    return ffi.cast('uintptr_t', data)


def _get_cffi_data():
    cffi = pytest.importorskip("cffi")
    ffi = cffi.FFI()
    return ffi.new('double *', 2.0)

