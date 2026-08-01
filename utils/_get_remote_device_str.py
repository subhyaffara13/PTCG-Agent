
def _get_remote_device_str(rank, device_type, num_devices_per_node):
    if device_type.lower() == "cpu":
        return f"rank:{rank}/{device_type}"
    elif device_type.lower() == "hpu":
        return f"rank:{rank}/{device_type}:{_get_device_module(device_type).current_device()}"
    else:
        return f"rank:{rank}/{device_type}:{rank % num_devices_per_node}"

