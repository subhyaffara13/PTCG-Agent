
def _group_nodes_from_linked_list(
    head: BaseSchedulerNode | None,
    tail: BaseSchedulerNode | None,
    next_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
) -> list[BaseSchedulerNode]:
    """
    Traverse doubly-linked list from head to tail and return nodes as a list.

    Args:
        head: Starting node of the segment
        tail: Ending node of the segment (inclusive)
        next_dict: Dictionary mapping each node to its next node

    Returns:
        List of nodes from head to tail (inclusive)
    """
    ret = []
    n = head
    while True:
        if n is not None:
            ret.append(n)
        if n == tail:
            break
        n = next_dict[n]  # type: ignore[index]
    return ret

