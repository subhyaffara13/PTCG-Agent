
def is_macos_or_newer(major: int, minor: int) -> bool:
    r"""Return a bool indicating whether MPS is running on given MacOS or newer."""
    return torch._C._mps_is_on_macos_or_newer(major, minor)

