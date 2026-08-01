
def dump_graph(graph: Graph, stdout: TextIO | None = None) -> None:
    """Dump the graph as a JSON string to stdout.

    This copies some of the work by process_graph()
    (sorted_components() and order_ascc()).
    """
    stdout = stdout or sys.stdout
    nodes = []
    sccs = sorted_components(graph)
    for i, ascc in enumerate(sccs):
        scc = order_ascc(graph, ascc.mod_ids)
        node = NodeInfo(i, scc)
        nodes.append(node)
    inv_nodes = {}  # module -> node_id
    for node in nodes:
        for mod in node.scc:
            inv_nodes[mod] = node.node_id
    for node in nodes:
        for mod in node.scc:
            state = graph[mod]
            size = 0
            if state.path:
                try:
                    size = os.path.getsize(state.path)
                except OSError:
                    pass
            node.sizes[mod] = size
            for dep in state.dependencies:
                if dep in state.priorities:
                    pri = state.priorities[dep]
                    if dep in inv_nodes:
                        dep_id = inv_nodes[dep]
                        if dep_id != node.node_id and (
                            dep_id not in node.deps or pri < node.deps[dep_id]
                        ):
                            node.deps[dep_id] = pri
    print("[" + ",\n ".join(node.dumps() for node in nodes) + "\n]", file=stdout)

