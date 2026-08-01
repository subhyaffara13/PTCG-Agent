
def has_hipsolver():
    rocm_version = _get_torch_rocm_version()
    # hipSOLVER is disabled on ROCM < 5.3
    return rocm_version >= (5, 3)

