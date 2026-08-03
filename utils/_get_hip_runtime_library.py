import sys

def _get_hip_runtime_library() -> ctypes.CDLL:
    # If ROCm python packages are available, query the OS-independent absolute
    # path to the library provided by those packages, including any version suffix.
    # See https://github.com/ROCm/TheRock/blob/main/docs/packaging/python_packaging.md#dynamic-library-resolution
    try:
        # pyrefly: ignore [import-error, missing-import]
        import rocm_sdk

        lib = ctypes.CDLL(str(rocm_sdk.find_libraries("amdhip64")[0]))
    except (ImportError, IndexError):
        if sys.platform == "win32":
            lib = ctypes.CDLL(f"amdhip64_{torch.version.hip[0]}.dll")
        else:  # Unix-based systems
            lib = ctypes.CDLL("libamdhip64.so")

    lib.cuGetErrorString = lib.hipGetErrorString  # type: ignore[attr-defined]
    lib.cuModuleLoadData = lib.hipModuleLoadData  # type: ignore[attr-defined]
    lib.cuModuleGetFunction = lib.hipModuleGetFunction  # type: ignore[attr-defined]
    lib.cuLaunchKernel = lib.hipModuleLaunchKernel  # type: ignore[attr-defined]
    lib.cuFuncSetAttribute = lib.hipFuncSetAttribute  # type: ignore[attr-defined]
    return lib

