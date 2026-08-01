
def _get_all_graph_pipes_helper(
    graph: DataPipeGraph, id_cache: set[int]
) -> list[DataPipe]:
    results: list[DataPipe] = []
    for dp_id, (datapipe, sub_graph) in graph.items():
        if dp_id in id_cache:
            continue
        id_cache.add(dp_id)
        results.append(datapipe)
        results.extend(_get_all_graph_pipes_helper(sub_graph, id_cache))
    return results

