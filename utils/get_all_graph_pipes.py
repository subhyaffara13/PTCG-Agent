
def get_all_graph_pipes(graph: DataPipeGraph) -> list[DataPipe]:
    return _get_all_graph_pipes_helper(graph, set())

