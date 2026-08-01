
def get_default_device() -> "torch.device":
    r"""Gets the default ``torch.Tensor`` to be allocated on ``device``"""
    global _GLOBAL_DEVICE_CONTEXT

    from torch.overrides import _get_current_function_mode_stack
    from torch.utils._device import DeviceContext

    def _get_device_with_index(device):
        if device.index is not None:
            return device
        else:
            # TODO: Call like get_device_index() method corresponding to
            # each device type
            return torch.tensor([]).device

    # Get device from any active DeviceContext.
    device_mode = next(
        filter(
            lambda mode: isinstance(mode, DeviceContext),
            reversed(_get_current_function_mode_stack()),
        ),
        None,
    )
    if device_mode:
        device = device_mode.device
        return _get_device_with_index(device)

    device_context = getattr(_GLOBAL_DEVICE_CONTEXT, "device_context", None)
    if device_context is not None:
        return _get_device_with_index(device_context.device)
    return torch.device("cpu")


def get_default_device() -> xc.Device:
  if isinstance(config.default_device.value, str):
    return xb.get_backend(config.default_device.value).local_devices()[0]
  else:
    return config.default_device.value or xb.local_devices()[0]

