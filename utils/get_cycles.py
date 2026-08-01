
def get_cycles(
    graph_dict: dict[str, set[str]], vertices: list[str] | None = None
) -> Sequence[list[str]]:
    """Return a list of detected cycles based on an ordered graph (i.e. keys are
    vertices and values are lists of destination vertices representing edges).
    """
    if not graph_dict:
        return ()
    result: list[list[str]] = []
    if vertices is None:
        vertices = list(graph_dict.keys())
    for vertice in vertices:
        _get_cycles(graph_dict, [], set(), result, vertice)
    return result

