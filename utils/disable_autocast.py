
def disable_autocast() -> Generator[None, None, None]:
    with ExitStack() as stack:
        autocast_enabled_devices = torch._C._autocast_supported_devices()
        for device_type in autocast_enabled_devices:
            if hasattr(torch, device_type):
                stack.enter_context(torch.amp.autocast(device_type, enabled=False))
        yield

