
def _code_compatible_with_device(device_cc: int, code_cc: int):
    if code_cc not in DEVICE_REQUIREMENT:
        warnings.warn(
            f"PyTorch was compiled with an unknown compute capability {code_cc // 10}.{code_cc % 10}. "
            + " Please create an issue on Github if this is a valid compute capability.",
            stacklevel=2,
        )
        return device_cc in _CompatInterval(start=code_cc)
    return device_cc in DEVICE_REQUIREMENT[code_cc]

