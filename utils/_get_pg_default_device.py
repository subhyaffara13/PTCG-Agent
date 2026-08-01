
def _get_pg_default_device(group: ProcessGroup | None = None) -> torch.device:
    """
    .. note:: This method will be deprecated, it only stays for
        backward-compatibility reason. Alternatives:

        - If you need to find a device for object collectives, please use
        `_get_object_coll_device(group)`.

        - If you need to query the device types supported by group, please use
        `_device_capability(group)`.

    Return the device type registered with ``group``.

    For example, if `init_process_group("nccl", ...)` was called, the returned
    value would be `torch.device("cuda")`.

    Errors out if no device has been registered.

    Args:
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.

    Returns:
        torch.device: The device type registered with ``group``.
    """

    warnings.warn(
        "`_get_pg_default_device` will be deprecated, it only stays for "
        "backward-compatibility reason. If you need to find a device for object "
        "collectives, please use `_get_object_coll_device`. If you need to query "
        "the device types supported by group, please use "
        "`_device_capability(group)`. ",
        stacklevel=2,
    )
    group = group or _get_default_group()

    if not isinstance(group, ProcessGroup):
        # Provide backward compatibility to cases where `group` passed in is
        # actually a Backend (like `ProcessGroupGloo`) rather than a
        # `ProcessGroup` in PT 2.0 sense
        warnings.warn(
            f"You are using a Backend {type(group)} as a ProcessGroup. "
            "This usage is deprecated since PyTorch 2.0. Please use a public API "
            "of PyTorch Distributed instead.",
            FutureWarning,
            stacklevel=3,
        )
        # Most users create Gloo with private API for object collectives
        return torch.device("cpu")

    """
    ``group._device_types`` is a property pybind that returns the devices
    ("cpu", "cuda", etc) supported by ``group``. Can be multiple if the
    ``group`` supports multiple devices.
    """
    devices = group._device_types

    if len(devices) == 1:
        # User fixed exactly one backend in `init_process_group`
        return devices[0]
    elif len(devices) == 0:
        raise RuntimeError(
            "Default device not found, because no backend has been registered "
            "with this ProcessGroup."
        )
    else:
        # There are multiple backends in this PG.
        if torch.device("cpu") in devices:
            rv = torch.device("cpu")
        else:
            rv = devices[0]
        warnings.warn(
            "Multiple backends are registered with this ProcessGroup. We cannot "
            f"determine which one is the default. Returning {rv}. "
            "Please consider using other APIs.",
            stacklevel=2,
        )
        return rv

