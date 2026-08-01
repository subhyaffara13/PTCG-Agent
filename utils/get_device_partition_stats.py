
def get_device_partition_stats(
    partitions: list[Partition], devices: list[Device]
) -> tuple[dict[Device, list[Partition]], dict[Device, int], list[Partition]]:
    """Given a list of partitions and a list of devices, returns:
    1. A mapping from device to partitions on it;
    2. A mapping from device to its remaining memory size;
    3. A list of partitions that do not have a device.
    """
    # logical id to device
    logical_id_to_device = get_logical_id_to_device(devices)
    # Track partitions on device
    device_to_partitions: dict[Device, list[Partition]] = {}
    # Track device's left mem size
    device_to_left_mem_bytes: dict[Device, int] = {}
    for d in devices:
        device_to_partitions[d] = []
        device_to_left_mem_bytes[d] = d.available_mem_bytes

    # Deal with the partitions that already have a device
    # and also collect all partitions without a device (no_device_partitions)
    no_device_partitions = []
    for partition in partitions:
        if partition.logical_device_ids != []:
            for logical_id in partition.logical_device_ids:
                device = logical_id_to_device[logical_id]
                device_to_partitions[device].append(partition)
                device_to_left_mem_bytes[device] -= partition.used_mem_bytes
        else:
            no_device_partitions.append(partition)

    return (
        device_to_partitions,
        device_to_left_mem_bytes,
        no_device_partitions,
    )

