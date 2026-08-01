
def get_node_to_partition_mapping(partitions: list[Partition]) -> dict[Node, int]:
    """Given a list of partitions,return node to partition mapping"""
    node_to_partition: dict[Node, int] = {}
    for partition in partitions:
        for node in partition.nodes:
            node_to_partition[node] = partition.partition_id
    return node_to_partition

