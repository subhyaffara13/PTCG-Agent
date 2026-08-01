
def _perform_double_linked_list_swap_sink_waits(
    candidate: BaseSchedulerNode,
    group_head: BaseSchedulerNode,
    group_tail: BaseSchedulerNode,
    prev_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    next_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    head: BaseSchedulerNode,
) -> BaseSchedulerNode:
    """
    Swap positions of candidate and group in doubly-linked list (sink_waits version).

    Transforms (moves candidate to the left):
    group_head_prev -> group_head...group_tail -> candidate -> candidate_next
    Into:
    group_head_prev -> candidate -> group_head...group_tail -> candidate_next

    Args:
        candidate: Node to swap with group
        group_head: First node of group
        group_tail: Last node of group
        prev_dict: Dictionary mapping nodes to their previous nodes
        next_dict: Dictionary mapping nodes to their next nodes
        head: Current head of the linked list

    Returns:
        New head of the linked list (may change if group_head was the head)
    """
    # 0: Update group_head's previous node
    group_head_prev = prev_dict[group_head]
    if group_head_prev:
        next_dict[group_head_prev] = candidate
    prev_dict[candidate] = group_head_prev

    # 2: Update candidate's next node
    candidate_next = next_dict[candidate]
    if candidate_next:
        prev_dict[candidate_next] = group_tail
    next_dict[group_tail] = candidate_next

    # 1: Link candidate to group_head
    prev_dict[group_head] = candidate
    next_dict[candidate] = group_head

    # Update head if group_head was the head
    if group_head == head:
        return candidate
    return head

