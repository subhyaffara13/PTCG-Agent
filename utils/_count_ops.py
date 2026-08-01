
def _count_ops(graph: fx.Graph) -> None:
    from collections import defaultdict

    cnt: dict[str, int] = defaultdict(int)
    for node in graph.nodes:
        if node.op == "call_function":
            cnt[node.target.__name__] += 1
    log.info("%s", sorted(cnt.items(), key=operator.itemgetter(1), reverse=True))

