
def _get_contiguous_fusible_spans(gm: fx.GraphModule) -> list[list[fx.Node]]:
    """Get contiguous spans of fusible nodes from the graph.

    Walks the graph in topological order and groups consecutive fusible
    nodes into spans. Non-fusible nodes act as span boundaries.
    """
    spans: list[list[fx.Node]] = []
    current_span: list[fx.Node] = []

    for node in gm.graph.nodes:
        if is_fusible_node(node):
            current_span.append(node)
        else:
            # Non-fusible node ends the current span
            if current_span:
                spans.append(current_span)
                current_span = []

    if current_span:
        spans.append(current_span)

    return spans

