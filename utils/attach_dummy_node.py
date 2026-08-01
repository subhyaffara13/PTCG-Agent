
def attach_dummy_node(node, name: str, runtime_object=_EMPTY_OBJECT_MARKER) -> None:
    """create a dummy node and register it in the locals of the given
    node with the specified name
    """
    _attach_local_node(node, build_dummy(runtime_object), name)

