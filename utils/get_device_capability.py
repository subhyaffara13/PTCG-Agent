from typing import Any

def get_device_capability(device: _device_t = None, /) -> dict[str, Any]:
    r"""Return the capability of the currently selected device.

    Args:
        device (:class:`torch.device`, str, int, optional): The device to query capabilities for
            :ref:`accelerator<accelerators>` device type. If not given,
            use :func:`torch.accelerator.current_device_index` by default.

    Returns:
        dict[str, Any]: A dictionary containing device capability information. The dictionary includes:
            - ``supported_dtypes`` (set(torch.dtype)): Set of PyTorch data types for which
              tensors can be allocated on the accelerator and type conversion across
              supported dtypes are supported. Any operator support outside of that
              is not guaranteed

    Examples:
        >>> # xdoctest: +SKIP("requires cuda")
        >>> # Query capabilities for current device
        >>> capabilities = torch.accelerator.get_device_capability("cuda:0")
        >>> print("Supported dtypes:", capabilities["supported_dtypes"])
    """
    device_index = _get_device_index(device, optional=True)
    # pyrefly: ignore [missing-attribute]
    return torch._C._accelerator_getDeviceCapability(device_index)


def get_device_capability(device: Device = None) -> tuple[int, int]:
    r"""Get the cuda capability of a device.

    Args:
        device (torch.device or int or str, optional): device for which to return the
            device capability. This function is a no-op if this argument is
            a negative integer. It uses the current device, given by
            :func:`~torch.cuda.current_device`, if :attr:`device` is ``None``
            (default).

    Returns:
        tuple(int, int): the major and minor cuda capability of the device
    """
    prop = get_device_properties(device)
    return prop.major, prop.minor


def get_device_capability(device: Device = None) -> tuple[int, int]:
    r"""Return capability of a given device as a tuple of (major version, minor version).

    Args:
        device (torch.device or int, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).
    """
    return torch._C._mtia_getDeviceCapability(_get_device_index(device, optional=True))


def get_device_capability(device: Device = None) -> dict[str, Any]:
    r"""Get the xpu capability of a device.

    Args:
        device (torch.device or int or str, optional): device for which to
            return the device capability. This function is a no-op if this
            argument is a negative integer. It uses the current device, given by
            :func:`~torch.xpu.current_device`, if :attr:`device` is ``None``
            (default).

    Returns:
        dict[str, Any]: the xpu capability dictionary of the device
    """
    props = get_device_properties(device)
    # Only keep attributes that are safe for dictionary serialization.
    serializable_types = (int, float, bool, str, type(None), list, tuple, dict)
    return {
        key: value
        for key in dir(props)
        if not key.startswith("__")
        and isinstance((value := getattr(props, key)), serializable_types)
    }

