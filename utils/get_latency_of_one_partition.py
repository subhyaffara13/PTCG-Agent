
def get_latency_of_one_partition(
    partition: Partition, node_to_latency_mapping: dict[Node, NodeLatency]
) -> PartitionLatency:
    """Given a partition and its nodes' latency, return a PartitionLatency for this partition"""

    def get_top_nodes(partition: Partition) -> list[Node]:
        """Given a partition, return a list of nodes on the top bfs level"""
        top_nodes: list[Node] = []
        for node in partition.nodes:
            # Skip placeholder and get_attr nodes
            if node.op in {"placeholder", "get_attr"}:
                continue
            input_nodes: dict[Node, None] = {}
            map_arg(node.args, input_nodes.setdefault)
            map_arg(node.kwargs, input_nodes.setdefault)
            # If a node has no input nodes in this partition,
            # or its input nodes in this partition are placeholders and get_attrs
            # this node is on the top bfs level in this partition
            if not any(
                n in partition.nodes and n.op not in {"placeholder", "get_attr"}
                for n in input_nodes
            ):
                top_nodes.append(node)
        return top_nodes

    def dfs_helper(node: Node, partition_latency) -> PartitionLatency:
        """Given a top node of a partition, this function returns
        the latency of the critical path in the partition
        """
        node_latency = node_to_latency_mapping[node]
        # Calculate the current overall latency of the partition
        overall_latency_sec = partition_latency.overall_latency_sec + max(
            node_latency.computer_latency_sec, node_latency.mem_latency_sec
        )
        # Update the mem latency of this path
        mem_latency_sec = (
            partition_latency.mem_latency_sec + node_latency.mem_latency_sec
        )
        # Update the compute latency of this path
        computer_latency_sec = (
            partition_latency.computer_latency_sec + node_latency.computer_latency_sec
        )
        # Get all users of this node that are in this partition
        users = set(node.users).intersection(partition.nodes)
        if users:
            max_latency = PartitionLatency(
                mem_latency_sec=0.0, computer_latency_sec=0.0, overall_latency_sec=0.0
            )
            for n in users:
                # Get new partition latency recursively
                new_partition_latency = dfs_helper(
                    n,
                    PartitionLatency(
                        mem_latency_sec, computer_latency_sec, overall_latency_sec
                    ),
                )
                if (
                    new_partition_latency.overall_latency_sec
                    > max_latency.overall_latency_sec
                ):
                    max_latency = new_partition_latency
            return max_latency
        # If there is no user, the node is at bottom of the partition
        return PartitionLatency(
            mem_latency_sec, computer_latency_sec, overall_latency_sec
        )

    # Main part starts
    # Get all top level nodes of this partition
    top_nodes = get_top_nodes(partition)
    critical_path_latency = PartitionLatency(
        mem_latency_sec=0.0, computer_latency_sec=0.0, overall_latency_sec=0.0
    )
    # Go through all top nodes and find the largest latency (critical pass latency)
    for node in top_nodes:
        partition_latency = dfs_helper(
            node,
            PartitionLatency(
                mem_latency_sec=0.0, computer_latency_sec=0.0, overall_latency_sec=0.0
            ),
        )
        if (
            partition_latency.overall_latency_sec
            > critical_path_latency.overall_latency_sec
        ):
            critical_path_latency = partition_latency
    return critical_path_latency

