
def _cxx_flags() -> str:
    """Returns the CXX_FLAGS used when building PyTorch."""
    return torch._C._cxx_flags()

