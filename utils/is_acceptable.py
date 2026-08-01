
def is_acceptable(tensor):
    if not torch._C._get_cudnn_enabled():
        return False
    if tensor.device.type != "cuda" or tensor.dtype not in CUDNN_TENSOR_DTYPES:
        return False
    if not is_available():
        warnings.warn(
            "PyTorch was compiled without cuDNN/MIOpen support. To use cuDNN/MIOpen, rebuild "
            "PyTorch making sure the library is visible to the build system.",
            stacklevel=2,
        )
        return False
    if not _init():
        warnings.warn(
            "cuDNN/MIOpen library not found. Check your {libpath}".format(
                libpath={"darwin": "DYLD_LIBRARY_PATH", "win32": "PATH"}.get(
                    sys.platform, "LD_LIBRARY_PATH"
                )
            ),
            stacklevel=2,
        )
        return False
    return True

