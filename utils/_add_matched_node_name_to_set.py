
def _add_matched_node_name_to_set(matched_node_pattern: NodePattern, s: set[str]):
    if isinstance(matched_node_pattern, Node):
        s.add(matched_node_pattern.name)
    elif isinstance(matched_node_pattern, (list, tuple)):  # noqa: UP038
        for maybe_node in matched_node_pattern:
            _add_matched_node_name_to_set(maybe_node, s)

