
def get_stream(node: Node) -> int | None:
    maybe_annotation = node.meta.get("custom", None)
    if maybe_annotation is not None:
        return node.meta["custom"].get("stream", None)
    else:
        return None


def getStream(group: str):
    handler = _metrics_map.get(group, _default_metrics_handler)
    return MetricStream(group, handler)

