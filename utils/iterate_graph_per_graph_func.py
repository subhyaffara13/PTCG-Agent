
def iterate_graph_per_graph_func(graph, per_graph_func, **func_args):
    """
    Iterate the graph including subgraphs calling the per_graph_func for each Graph.
    :param graph: Graph to iterate
    :param per_graph_func: Function to call for each graph. Signature is fn(graph: onnx:GraphProto, **kwargs)
    :param func_args: The keyword args to pass through.
    """

    per_graph_func(graph, **func_args)

    for node in graph.node:
        # recurse into subgraph for control flow nodes (Scan/Loop/If)
        for attr in node.attribute:
            if attr.HasField("g"):
                iterate_graph_per_graph_func(attr.g, per_graph_func, **func_args)

