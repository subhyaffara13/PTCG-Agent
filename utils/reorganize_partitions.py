
def reorganize_partitions(partitions: list[Partition]) -> None:
    """Given a list of partitions, reorganize partition id,
    its parents and its children for each partition
    """
    # Rearrange partition ids
    for i, partition in enumerate(partitions):
        partition.partition_id = i
    set_parents_and_children(partitions)
    return

