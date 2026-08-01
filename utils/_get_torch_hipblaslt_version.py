
def _get_torch_hipblaslt_version():
    if not TEST_WITH_ROCM:
        return None
    try:
        # Access through direct C binding
        # versionHipBLASLt returns: MAJOR * 10000 + MINOR * 100 + PATCH
        version_int = torch._C._cuda_getHipblasltVersion()
        if version_int is None or version_int == 0:
            return None
        major = version_int // 10000
        minor = (version_int % 10000) // 100
        patch = version_int % 100
        return (major, minor, patch)
    except (AttributeError, RuntimeError):
        return None

