
def _init_inter_node_process_group(
    global_process_group: dist.ProcessGroup,
    num_devices_per_node: int,
) -> dist.ProcessGroup:
    """
    Return an inter-node process group where each contained rank has the same local rank.

    For example, given each row is a distinct node:
    0  1  2  3  4  5  6  7
    8  9 10 11 12 13 14 15
    This API would return inter-node process group [0, 8], [1, 9], [2, 10], and so forth
    depending on the process's rank. For example, rank 1 would get [1, 9], rank 5
    would get [5, 13].
    """
    # the inter-node pg that is returned
    inter_node_pg = None
    sharding_backend = dist.get_backend(global_process_group)
    world_size = dist.get_world_size(global_process_group)
    # Assuming fully homogeneous setup
    num_nodes = world_size // num_devices_per_node
    my_local_rank = dist.get_rank(global_process_group) % num_devices_per_node
    for local_rank in range(num_devices_per_node):
        ranks_for_inter_group = [
            local_rank + (i * num_devices_per_node) for i in range(num_nodes)
        ]
        # every rank always needs to call dist.new_group
        grp = dist.new_group(ranks=ranks_for_inter_group, backend=sharding_backend)
        if local_rank == my_local_rank:
            inter_node_pg = grp

    if inter_node_pg is None:
        raise AssertionError(
            f"{my_local_rank} expected to assign inter-node pg, but did not"
        )
    return inter_node_pg

