
def load_signer_lib(signer_lib_path):
    _LOGGER.debug("loading signer library from %s", signer_lib_path)

    # winmode parameter is only available for python 3.8+.
    lib = (
        ctypes.CDLL(signer_lib_path, winmode=0)
        if sys.version_info >= (3, 8) and os.name == "nt"
        else ctypes.CDLL(signer_lib_path)
    )

    # Set up types for:
    # func GetCertPemForPython(configFilePath *C.char, certHolder *byte, certHolderLen int)
    lib.GetCertPemForPython.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    # Returns: certLen
    lib.GetCertPemForPython.restype = ctypes.c_int

    # Set up types for:
    # func SignForPython(configFilePath *C.char, digest *byte, digestLen int,
    #     sigHolder *byte, sigHolderLen int)
    lib.SignForPython.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    # Returns: the signature length
    lib.SignForPython.restype = ctypes.c_int

    return lib

