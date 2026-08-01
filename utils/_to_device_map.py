
def _to_device_map(
    device_map: dict[DeviceType, DeviceType],
) -> dict[torch.device, torch.device]:
    full_device_map: dict[torch.device, torch.device] = {}
    reverse_map: dict[torch.device, torch.device] = {}
    for k, v in device_map.items():
        k, v = torch.device(k), torch.device(v)
        if v in reverse_map:
            raise ValueError(
                "`device_map` only supports 1-to-1 mapping, "
                f"trying to map {k} and {reverse_map[v]} to {v}"
            )
        full_device_map[k] = v
        reverse_map[v] = k
    return full_device_map

