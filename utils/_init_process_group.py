
def _init_process_group(store, rank, world_size):
    # Initialize ProcessGroup.
    process_group_timeout = rpc_constants.DEFAULT_PROCESS_GROUP_TIMEOUT

    # We're using a bunch of private APIs here since `new_group` requires the
    # default group to be initialized.
    group = dist.ProcessGroupGloo(store, rank, world_size, process_group_timeout)

    if group is None:
        raise AssertionError("Failed to initialize default ProcessGroup.")

    if (rank != -1) and (rank != group.rank()):
        raise RuntimeError(f"rank argument {rank} doesn't match pg rank {group.rank()}")
    if (world_size != -1) and (world_size != group.size()):
        raise RuntimeError(
            f"world_size argument {world_size} doesn't match pg size {group.size()}"
        )
    return group

