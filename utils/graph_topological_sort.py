
def graph_topological_sort(graph):
    deps_count = [0] * len(graph.node)  # dependency count of each node
    deps_to_nodes = {}  # input to node indice
    sorted_nodes = []  # initialize sorted_nodes
    for node_idx, node in enumerate(graph.node):
        # CANNOT use len(node.input) directly because input can be optional
        deps_count[node_idx] = sum(1 for _ in node.input if _)
        if deps_count[node_idx] == 0:  # Constant doesn't depend on any inputs
            sorted_nodes.append(graph.node[node_idx])
            continue

        for input_name in node.input:
            if input_name not in deps_to_nodes:
                deps_to_nodes[input_name] = [node_idx]
            else:
                deps_to_nodes[input_name].append(node_idx)

    # Note: this logic only applies to top level graph since a sub graph could use intializer from parent graph
    initializer_names = [init.name for init in graph.initializer]
    graph_input_names = [input.name for input in graph.input]
    input_names = initializer_names + graph_input_names
    input_names.sort()
    prev_input_name = None
    for input_name in input_names:
        if prev_input_name == input_name:
            continue

        prev_input_name = input_name
        if input_name in deps_to_nodes:
            for node_idx in deps_to_nodes[input_name]:
                deps_count[node_idx] = deps_count[node_idx] - 1
                if deps_count[node_idx] == 0:
                    sorted_nodes.append(graph.node[node_idx])

    start = 0
    end = len(sorted_nodes)

    while start < end:
        for output in sorted_nodes[start].output:
            if output in deps_to_nodes:
                for node_idx in deps_to_nodes[output]:
                    deps_count[node_idx] = deps_count[node_idx] - 1
                    if deps_count[node_idx] == 0:
                        sorted_nodes.append(graph.node[node_idx])
                        end = end + 1
        start = start + 1

    assert end == len(graph.node), "Graph is not a DAG"
    graph.ClearField("node")
    graph.node.extend(sorted_nodes)

