
def _get_autocast_kwargs(device_type="cuda"):
    if torch.amp.is_autocast_available(device_type):
        device_autocast_kwargs = {
            "enabled": torch.is_autocast_enabled(device_type),
            "dtype": torch.get_autocast_dtype(device_type),
            "cache_enabled": torch.is_autocast_cache_enabled(),
        }
    else:
        device_autocast_kwargs = None

    cpu_autocast_kwargs = {
        "enabled": torch.is_autocast_enabled('cpu'),
        "dtype": torch.get_autocast_dtype('cpu'),
        "cache_enabled": torch.is_autocast_cache_enabled(),
    }

    return device_autocast_kwargs, cpu_autocast_kwargs

