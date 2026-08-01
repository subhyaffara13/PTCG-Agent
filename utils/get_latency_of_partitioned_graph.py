
def get_latency_of_partitioned_graph(
    partitions: list[Partition],
    partition_to_latency_mapping: dict[Partition, PartitionLatency],
    transfer_rate_bytes_per_sec: float,
):
    """Given all partitions in a graph, find the critical path among all partitions
    and return its latency as the latency of the whole graph
    """

    def dfs_helper(partition: Partition, latency_so_far_sec: float) -> float:
        """This function helps to recursively get the latency of a path of partitions"""
        # Update latency by adding current partition's latency
        latency_so_far_sec += partition_to_latency_mapping[
            partition
        ].overall_latency_sec

        if partition.children:
            max_latency_sec = 0.0
            for child in partition.children:
                # Calculate latency between
                comm_latency_sec = get_comm_latency_between(
                    partition, child, transfer_rate_bytes_per_sec
                )
                new_latency_sec = dfs_helper(
                    child, latency_so_far_sec + comm_latency_sec
                )
                if new_latency_sec > max_latency_sec:
                    max_latency_sec = new_latency_sec
            return max_latency_sec
        return latency_so_far_sec

    def get_top_partitions(partitions: list[Partition]) -> list[Partition]:
        """This function is to return all the partitions without parents
        as the starting points of all the paths
        """
        # If a partition has no parents, then it is a top partition
        top_partitions = [
            partition for partition in partitions if len(partition.parents) == 0
        ]
        return top_partitions

    top_partitions = get_top_partitions(partitions)
    critical_path_latency_sec = 0.0
    for partition in top_partitions:
        latency_sec = dfs_helper(partition, 0.0)
        if latency_sec > critical_path_latency_sec:
            critical_path_latency_sec = latency_sec
    return critical_path_latency_sec

