
def is_fsdp_reduce_scatter(node: torch.fx.Node) -> bool:
    """
    Check if a reduce_scatter node is FSDP-related by verifying its output flows
    directly to graph outputs through only unary ops (e.g., to_copy, wait).
    """
    if not is_reduce_scatter_tensor(node):
        return False

    visited: OrderedSet[torch.fx.Node] = OrderedSet()
    stack = [node]

    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)

        for user in curr.users:
            if user.op == "output":
                continue
            # Non-unary op means computation with external data
            if len(user.all_input_nodes) != 1:
                return False
            stack.append(user)

    return True

