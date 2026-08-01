
def dump_line_checking_stats(path: str, graph: Graph) -> None:
    """Dump per-line expression type checking stats."""
    with open(path, "w") as f:
        for id in sorted(graph):
            if not graph[id].per_line_checking_time_ns:
                continue
            f.write(f"{id}:\n")
            for line in sorted(graph[id].per_line_checking_time_ns):
                line_time = graph[id].per_line_checking_time_ns[line]
                f.write(f"{line:>5} {line_time/1000:8.1f}\n")

