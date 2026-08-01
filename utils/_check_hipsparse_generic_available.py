
def _check_hipsparse_generic_available():
    if not TEST_WITH_ROCM:
        return False
    if not torch.version.hip:
        return False

    rocm_version = str(torch.version.hip)
    rocm_version = rocm_version.split("-", maxsplit=1)[0]    # ignore git sha
    rocm_version_tuple = tuple(int(x) for x in rocm_version.split("."))
    return not (rocm_version_tuple is None or rocm_version_tuple < (5, 1))

