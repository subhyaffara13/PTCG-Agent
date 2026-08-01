
def reset_partition_device(partitions):
    for partition in partitions:
        partition.logical_device_ids = []

