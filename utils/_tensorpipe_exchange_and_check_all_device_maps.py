
def _tensorpipe_exchange_and_check_all_device_maps(
    my_name, my_device_count, my_device_maps, my_devices, group
):
    gathered: list[
        tuple[str, int, dict[str, dict[torch.device, torch.device]], list[torch.device]]
    ] = [("", 0, {}, []) for _ in range(group.size())]
    dist.all_gather_object(
        gathered, (my_name, my_device_count, my_device_maps, my_devices), group
    )
    all_names = [name for name, _, _, _ in gathered]
    all_device_counts = {name: count for name, count, _, _ in gathered}
    all_device_maps = {name: map_ for name, _, map_, _ in gathered}
    all_devices = {name: devices for name, _, _, devices in gathered}

    _validate_device_maps(all_names, all_device_counts, all_device_maps, all_devices)

    # passed all checked, construct reverse mapping and get list of devices handled by this agent
    reverse_device_maps = _create_reverse_mapping(my_name, all_names, all_device_maps)
    my_devices = _create_device_list(my_devices, my_device_maps, reverse_device_maps)
    return reverse_device_maps, my_devices

