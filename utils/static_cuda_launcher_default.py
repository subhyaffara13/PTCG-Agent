
def static_cuda_launcher_default() -> bool:
    STATIC_CUDA_LAUNCHER_VERSION = 2

    if "TORCHINDUCTOR_USE_STATIC_CUDA_LAUNCHER" in os.environ:
        return os.environ.get("TORCHINDUCTOR_USE_STATIC_CUDA_LAUNCHER") == "1"
    elif is_fbcode():
        version = torch._utils_internal.justknobs_getval_int(
            "pytorch/inductor:static_cuda_launcher_version"
        )
        return version <= STATIC_CUDA_LAUNCHER_VERSION
    else:
        # Default true in OSS
        return True

