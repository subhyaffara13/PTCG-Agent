
def dump_timing_stats(path: str, graph: Graph) -> None:
    """Dump timing stats for each file in the given graph."""
    with open(path, "w") as f:
        for id in sorted(graph):
            f.write(f"{id} {graph[id].time_spent_us}\n")

