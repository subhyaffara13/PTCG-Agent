
def _device_type_to_key(device_type: str) -> str:
    if device_type == "default":
        # This is technically not correct, because although all device_type
        # DispatchKeys are included in CompositeExplicitAutograd,
        # not everything in CompositeExplicitAutograd is associated with a
        # device_type. I don't really care that much about the difference.
        return "CompositeExplicitAutograd"
    return torch._C._dispatch_key_for_device(device_type)

