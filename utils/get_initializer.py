
def get_initializer(name, graph_path: list[GraphProto]) -> tuple[TensorProto, GraphProto]:
    for gid in range(len(graph_path) - 1, -1, -1):
        graph = graph_path[gid]
        for tensor in graph.initializer:
            if tensor.name == name:
                return tensor, graph
    return None, None

