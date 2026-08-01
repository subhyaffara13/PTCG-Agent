
def _get_hiprtc_library() -> ctypes.CDLL:
    try:
        # pyrefly: ignore [import-error, missing-import]
        import rocm_sdk

        lib = ctypes.CDLL(str(rocm_sdk.find_libraries("hiprtc")[0]))
    except (ImportError, IndexError):
        if sys.platform == "win32":
            version_str = "".join(
                ["0", torch.version.hip[0], "0", torch.version.hip[2]]
            )
            lib = ctypes.CDLL(f"hiprtc{version_str}.dll")
        else:
            lib = ctypes.CDLL("libhiprtc.so")

    # Provide aliases for HIP RTC functions to match NVRTC API
    lib.nvrtcGetErrorString = lib.hiprtcGetErrorString  # type: ignore[attr-defined]
    lib.nvrtcCreateProgram = lib.hiprtcCreateProgram  # type: ignore[attr-defined]
    lib.nvrtcDestroyProgram = lib.hiprtcDestroyProgram  # type: ignore[attr-defined]
    lib.nvrtcCompileProgram = lib.hiprtcCompileProgram  # type: ignore[attr-defined]
    lib.nvrtcGetCUBINSize = lib.hiprtcGetCodeSize  # type: ignore[attr-defined]
    lib.nvrtcGetCUBIN = lib.hiprtcGetCode  # type: ignore[attr-defined]
    lib.nvrtcGetProgramLogSize = lib.hiprtcGetProgramLogSize  # type: ignore[attr-defined]
    lib.nvrtcGetProgramLog = lib.hiprtcGetProgramLog  # type: ignore[attr-defined]
    lib.nvrtcAddNameExpression = lib.hiprtcAddNameExpression  # type: ignore[attr-defined]
    lib.nvrtcGetLoweredName = lib.hiprtcGetLoweredName  # type: ignore[attr-defined]
    return lib

