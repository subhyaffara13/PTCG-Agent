
def _create_reverse_mapping(my_name, all_names, all_device_maps):
    reverse_device_maps: dict[str, dict[torch.device, torch.device]] = {}
    for node in all_names:
        if my_name in all_device_maps[node]:
            reverse_device_maps[node] = {
                v: k for k, v in all_device_maps[node][my_name].items()
            }
    return reverse_device_maps

