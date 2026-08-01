
def make_dim_param_fixed(graph: onnx.GraphProto, param_name: str, value: int):
    """
    Iterate all values in the graph, replacing dim_param in a tensor shape with the provided value.
    :param graph: GraphProto to update
    :param param_name: dim_param to set
    :param value: value to use
    """
    iterate_graph_per_graph_func(graph, _replace_symbolic_dim_value, dim_param=param_name, value=value)

