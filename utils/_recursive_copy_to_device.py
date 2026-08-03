from typing import Any

def _recursive_copy_to_device(
    value: Any,
    non_blocking: bool,
    device: torch.device,
) -> Any:
    r"""
    Recursively searches lists, tuples, dicts and copies tensors to device if possible.

    Non-tensor values are passed as-is in the result.

    .. note::
        These are all copies, so if there are two objects that reference
        the same object, then after this call, there will be two different objects
        referenced on the device.
    """
    if isinstance(value, torch.Tensor):
        return value.to(device, non_blocking=non_blocking)

    if isinstance(value, (list, tuple)):
        values = [
            _recursive_copy_to_device(val, non_blocking=non_blocking, device=device)
            for val in value
        ]
        return values if isinstance(value, list) else tuple(values)

    if isinstance(value, collections.abc.Mapping):
        return {
            key: _recursive_copy_to_device(
                val, non_blocking=non_blocking, device=device
            )
            for key, val in value.items()
        }

    return value

