
def remove_invalid_dim_values(graph: onnx.GraphProto):
    """
    Iterate the graph and subgraphs, unsetting any dim_value entries that have a value of less than 1.
    These are typically erroneously inserted by a converter to represent a dynamic dimension.
    :param graph: GraphProto to update
    """
    iterate_graph_per_graph_func(graph, _remove_invalid_dim_values_impl)

