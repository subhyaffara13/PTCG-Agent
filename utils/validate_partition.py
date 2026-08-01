
def validate_partition(partition: NodeList) -> bool:
    # verify the partition doesn't form a dependency cycle in the original graph
    # returns True for valid partition, False for invalid

    partition_set = set(partition)

    outputs: NodeList = []
    for node in partition_set:
        for user_node in node.users:
            if user_node not in partition_set:
                # external user node, need to expose as an output
                outputs.append(user_node)

    # Perform BFS on the partition outputs.
    # If it reaches a node within the partition, then it found a cycle.
    # This function takes the ownership of `root_nodes` and may modify it.
    def bfs_find_cycle(root_nodes: NodeList) -> bool:
        # Set used to exclude nodes that have already been visited.
        # If a node has been visited, that node and all its children have
        # been checked for cycles.
        visited: NodeSet = set()

        # Start with `root_nodes` and traverse through (toward child nodes)
        # their connected sub-graph. Nodes in `visited` won't be added
        # to `queue` again.
        queue: NodeList = root_nodes
        while queue:
            current = queue.pop()
            visited.add(current)
            if current in partition_set:
                # Started from partition's `output` nodes, and reached
                # another node in partition. Cycle!
                return True
            for user_node in current.users:
                if user_node in visited:
                    continue
                queue.append(user_node)
        # `root_nodes` don't cause cycle.
        return False

    # Use all output nodes as roots to traverse
    # the graph to check cycles.
    if bfs_find_cycle(outputs):
        return False

    return True

