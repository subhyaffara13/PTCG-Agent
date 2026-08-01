
def get_bfs_level_partition(partitions: list[Partition]) -> None:
    """Given a list of partitions,
    mark the bfs level for each partition
    """
    current_level: set[Partition] = set()
    visited: set[Partition] = set()
    for partition in partitions:
        # If a partition has no parent, it should be in root level
        if len(partition.parents) == 0:
            current_level.add(partition)
    next_level: set[Partition] = set()
    level = 0
    # bfs
    while current_level:
        partition = current_level.pop()
        partition.bfs_level = level
        visited.add(partition)
        children = partition.children
        for child in children:
            if child not in next_level:
                next_level.add(child)
        if not current_level:
            current_level = next_level.copy()
            next_level = set()
            level += 1
    return

