
def skip_if_rocm_ver_lessthan_multiprocess(version=None):
    """Skips a test for ROCm based on ROCm ver - multiprocess UTs"""

    def decorator(func):
        reason = None
        if TEST_WITH_ROCM:
            rocm_version = str(torch.version.hip)
            rocm_version = rocm_version.split("-", maxsplit=1)[0]  # ignore git sha
            rocm_version_tuple = tuple(int(x) for x in rocm_version.split("."))
            if (
                rocm_version_tuple is None
                or version is None
                or rocm_version_tuple < tuple(version)
            ):
                reason = f"skip_if_rocm_ver_lessthan_multiprocess: ROCm {rocm_version_tuple} is available but {version} required"

        return unittest.skipIf(reason is not None, reason)(func)

    return decorator

