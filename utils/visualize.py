
def visualize(graph, name_prefix="", pb_graph=None, executors_it=None):
    """Visualizes an independent graph, or a graph executor."""
    value_map = {}
    pb_graph = pb_graph or graph_pb2.GraphDef()

    if isinstance(graph, torch._C.GraphExecutorState):
        visualize_graph_executor(
            graph, name_prefix, pb_graph, partial(visualize, pb_graph=pb_graph)
        )
        return pb_graph

    # Set up an input node
    pb_graph.node.add(op="input", name=name_prefix + "input")
    for i, value in enumerate(graph.param_node().outputs()):
        value_map[value.unique()] = name_prefix + "input:" + str(i)

    visualize_rec(graph, value_map, name_prefix, pb_graph, executors_it)

    # Gather all outputs
    return_node = pb_graph.node.add(op="output", name=name_prefix + "output")
    for value in graph.return_node().inputs():
        return_node.input.append(value_map[value.unique()])

    return pb_graph

