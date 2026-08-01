
def set_current_meta(node: Node, pass_name: str = "") -> Iterator[None]:
    global current_meta
    if should_preserve_node_meta and node.meta:
        saved_meta = current_meta
        try:
            current_meta = node.meta.copy()

            # Update the "from_node" field in current_meta for provenance tracking.
            # Instead of appending, overwrite the "from_node" field because current_meta
            # will be assigned to the new node. The new NodeSource(node, ...) will
            # include the information from the previous current_meta["from_node"].
            current_meta["from_node"] = [
                NodeSource(node, pass_name, NodeSourceAction.CREATE)
            ]
            yield
        finally:
            current_meta = saved_meta
    else:
        yield

