
def expand_device_map(device_map: dict | None, param_names: list[str]):
    """
    Expand a device map to return the correspondence parameter name to device.
    """
    if device_map is None:
        return dict.fromkeys(param_names, "cpu")

    # Here, we first sort by number of submodules, then length of the full string, to make sure to match correctly
    device_map_regex = re.compile(
        "|".join(rf"({k})" for k in sorted(device_map.keys(), key=lambda x: (x.count("."), len(x)), reverse=True))
    )
    new_device_map = {}
    for param in param_names:
        device_match = device_map_regex.match(param)
        new_device_map[param] = device_map[device_match.group()] if device_match else device_map.get("", "cpu")

    return new_device_map

