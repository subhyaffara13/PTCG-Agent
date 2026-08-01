
def topological_sort_dfs(nodes: list[BaseSchedulerNode]) -> list[BaseSchedulerNode]:
    """
    This is a DFS topological sort. The setup is similar to `topological_sort_schedule`
    in scheduler.py. The difference is the order nodes are visited in the outer loop.
    In `topological_sort_schedule`, nodes are visited in their original order.
    In this function, nodes are visited based on their priority -- for each node, we
    compute the total memory of all buffers it reads from or writes to, and we visit
    the nodes in ascending order of this priority.
    """
    seen: OrderedSet[BaseSchedulerNode] = OrderedSet()
    name_to_node: dict[str, BaseSchedulerNode] = dict()
    result: list[BaseSchedulerNode] = []
    size_with_reads: dict[BaseSchedulerNode, int] = dict()

    def visit(n: BaseSchedulerNode) -> None:
        if n not in seen:
            seen.add(n)
            dep_nodes = [
                name_to_node[dep.name]
                for dep in n.unmet_dependencies
                if dep.name in name_to_node
            ]
            for node in sorted(
                dep_nodes, key=lambda n: (size_with_reads[n], n.mpi_node.index)
            ):
                visit(node)
            result.append(n)

    for node in nodes:
        for name in node.get_buffer_names():
            name_to_node[name] = node

    for node in nodes:
        size_with_reads[node] = node.mpi_node.size + sum(
            pred_buf.mpi_buffer.size_free for pred_buf in node.mpi_node.pred_buffers
        )
    for node in sorted(nodes, key=lambda n: (size_with_reads[n], n.mpi_node.index)):
        visit(node)

    return result

