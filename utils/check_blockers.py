
def check_blockers(graph: Graph, scc: list[str]) -> None:
    for module in scc:
        graph[module].check_blockers()

