
def _check_single_device_module(
    module: nn.Module,
    ignored_params: set[nn.Parameter],
    device_id: int | torch.device | None,
) -> None:
    """
    Raise an error if ``module`` has original parameters on multiple devices, ignoring the parameters in ``ignored_params``.

    Thus, after this method, the
    module must be either fully on the CPU or fully on a non-CPU device.
    """
    devices = {param.device for param in _get_orig_params(module, ignored_params)}
    # We allow module to be partially on CPU and partially on GPU if device_id is not
    # None, since the device_id arg will result in the CPU portion being moved to
    # GPU. This is useful in cases where part of the module may be parallelized
    # by another algorithm and may already be on GPU. We'd like to enforce device_id
    # to not be None, otherwise we'd flatten parameters in a mixed module which is
    # not supported.
    if len(devices) == 2 and torch.device("cpu") in devices:
        if device_id is None:
            raise RuntimeError(
                "To support a module with both CPU and GPU params, "
                "please pass in device_id argument."
            )
    elif len(devices) > 1:
        raise RuntimeError(
            f"FSDP only supports single device modules but got params on {devices}"
        )

