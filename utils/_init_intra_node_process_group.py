
def _init_intra_node_process_group(num_devices_per_node: int) -> dist.ProcessGroup:
    """
    Return a process group across the current node.

    For example, given each row is a distinct node:
    0  1  2  3  4  5  6  7
    8  9 10 11 12 13 14 15
    This API would return an intra-node subgroup across
    [0, 1, ..., 7] or [8, 9, ..., 15] depending on the process's rank.
    For example, rank 3 would get [0, 1, ..., 7].
    """
    intra_node_subgroup, _ = dist.new_subgroups(num_devices_per_node)
    return intra_node_subgroup

