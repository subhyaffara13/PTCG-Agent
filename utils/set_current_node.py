
def set_current_node(node: torch.fx.Node) -> Generator[None, None, None]:
    old = get_current_node()
    _current_node.value = node
    try:
        yield
    finally:
        _current_node.value = old

