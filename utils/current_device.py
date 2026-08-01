
def current_device() -> str:
    r"""Returns current device for cpu. Always 'cpu'.

    N.B. This function only exists to facilitate device-agnostic code
    """
    return "cpu"


def current_device() -> int:
    r"""Return the index of a currently selected device."""
    _lazy_init()
    return torch._C._cuda_getDevice()


def current_device() -> int:
    r"""Return the index of a currently selected device."""
    # pyrefly: ignore [missing-attribute]
    return torch._C._mtia_getDevice()


def current_device() -> int:
    r"""Return the index of a currently selected device."""
    _lazy_init()
    return torch._C._xpu_getDevice()

