
def propagate_general_copy_metadata_ignore_broadcast(out_node: Node) -> _HandlerRetType:
    return propagate_general_copy_metadata(out_node, ignore_broadcast=True)  # type: ignore[call-arg]

