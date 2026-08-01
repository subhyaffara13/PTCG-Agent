
def _get_restore_location(map_location):
    if map_location is None:
        restore_location = default_restore_location
    elif isinstance(map_location, dict):

        def restore_location(storage, location):
            location = map_location.get(location, location)
            return default_restore_location(storage, location)

    elif isinstance(map_location, (str, bytes)):

        def restore_location(storage, location):
            return default_restore_location(storage, map_location)

    elif isinstance(map_location, torch.device):

        def restore_location(storage, location):
            return default_restore_location(storage, str(map_location))

    else:

        def restore_location(storage, location):
            result = map_location(storage, location)
            if result is None:
                result = default_restore_location(storage, location)
            return result

    return restore_location


def _get_restore_location(device):
    """Return the map_location location.

    Used for rebuild functions where the tensor device is distinct from the storage
    """

    map_location = torch.serialization._serialization_tls.map_location
    if map_location is None:
        return device
    else:
        if isinstance(map_location, dict):
            return map_location.get(device, device)
        elif isinstance(map_location, (str, torch.device)):
            return map_location
        else:
            if not callable(map_location):
                raise AssertionError(
                    f"expected callable map_location, got {type(map_location).__name__}"
                )
            raise RuntimeError(
                "Callable map_location not supported with _rebuild_wrapper_subclass "
                "or _rebuild_device_tensor_from_numpy"
            )

