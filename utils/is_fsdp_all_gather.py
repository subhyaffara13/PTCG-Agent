
def is_fsdp_all_gather(
    node: torch.fx.Node,
    all_node_ancestors: dict[torch.fx.Node, OrderedSet[torch.fx.Node]],
) -> bool:
    """
    Check if the node is a FSDP-related all_gather by its recursive ancestors.
    On the path from the all-gather to its originate placeholder, there should not be any compute node
    So there should be ONLY ONE placeholder in its recursive ancestors.
    """
    if not is_all_gather_into_tensor(node):
        return False

    seen_placeholders = 0
    for ancestor in all_node_ancestors[node]:
        if ancestor.op == "placeholder":
            seen_placeholders += 1

    return seen_placeholders == 1


def is_fsdp_all_gather(n):
    assert is_all_gather(n)
    while len(n.all_input_nodes) == 1:
        n = n.all_input_nodes[0]
        if n.op == "placeholder":
            return True
    return False

