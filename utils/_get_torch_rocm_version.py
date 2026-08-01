
def _get_torch_rocm_version():
    if not TEST_WITH_ROCM or torch.version.hip is None:
        return (0, 0)
    rocm_version = str(torch.version.hip)
    rocm_version = rocm_version.split("-", maxsplit=1)[0]    # ignore git sha
    return tuple(int(x) for x in rocm_version.split("."))

