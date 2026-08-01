
def combine_two_partitions(
    partition_0: Partition, partition_1: Partition, partitions: list[Partition]
) -> None:
    """Given a list of partitions and its two partitions,
    combine these two partitions into a new one appending to the partitions
    and remove the previous two partitions from the list of partitions
    """
    partition = Partition(len(partitions))
    partition.nodes = partition_0.nodes.union(partition_1.nodes)
    partition.recalculate_mem_size()
    partitions.append(partition)
    partitions.remove(partition_0)
    partitions.remove(partition_1)
    reorganize_partitions(partitions)
    return

