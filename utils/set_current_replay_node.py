
def set_current_replay_node(node: Node | None) -> Iterator[None]:
    """
    Set the currently replay node. If `current_replay_node` is not None,
    then we're re-generating the `current_replay_node` in FunctionalTensorMode.
    """
    # See [Note] annotation for more details.
    global current_replay_node
    saved_current_replay_node = current_replay_node
    try:
        current_replay_node = node
        yield
    finally:
        current_replay_node = saved_current_replay_node

