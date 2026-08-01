
def _perform_double_linked_list_swap(
    candidate: BaseSchedulerNode,
    group_head: BaseSchedulerNode,
    group_tail: BaseSchedulerNode,
    prev_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    next_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    head: BaseSchedulerNode,
) -> BaseSchedulerNode:
    """
    Swap positions of candidate and group in doubly-linked list.

    Transforms:
    candidate_prev -> candidate -> group_head...group_tail -> group_tail_next
    Into:
    candidate_prev -> group_head...group_tail -> candidate -> group_tail_next

    Args:
        candidate: Node to swap with group
        group_head: First node of group
        group_tail: Last node of group
        prev_dict: Dictionary mapping nodes to their previous nodes
        next_dict: Dictionary mapping nodes to their next nodes
        head: Current head of the linked list

    Returns:
        New head of the linked list (may change if candidate was the head)
    """
    # 0: Update candidate's previous node
    candidate_prev = prev_dict[candidate]
    if candidate_prev:
        next_dict[candidate_prev] = group_head
    prev_dict[group_head] = candidate_prev

    # 2: Update group_tail's next node
    group_tail_next = next_dict[group_tail]
    if group_tail_next:
        prev_dict[group_tail_next] = candidate
    next_dict[candidate] = group_tail_next

    # 1: Link group_tail to candidate
    prev_dict[candidate] = group_tail
    next_dict[group_tail] = candidate

    # Update head if candidate was the head
    if head == candidate:
        return group_head
    return head

