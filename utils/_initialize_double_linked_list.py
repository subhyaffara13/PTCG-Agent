
def _initialize_double_linked_list(
    snodes: list[BaseSchedulerNode],
) -> tuple[
    dict[BaseSchedulerNode, BaseSchedulerNode | None],
    dict[BaseSchedulerNode, BaseSchedulerNode | None],
    BaseSchedulerNode,
]:
    """Create double-linked list structure from snodes"""
    _prev = {}
    _next = {}
    for i, snode in enumerate(snodes):
        _prev[snode] = snodes[i - 1] if i > 0 else None
        _next[snode] = snodes[i + 1] if i < len(snodes) - 1 else None
    _head = snodes[0]
    return _prev, _next, _head

