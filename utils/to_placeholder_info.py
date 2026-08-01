
def to_placeholder_info(placeholder_node: torch.fx.Node) -> PlaceholderInfo:
    name = placeholder_node.name
    stack_trace = placeholder_node.meta.get("stack_trace", None)
    users = []
    mutating_use_stack_trace = None
    # Only recurse to users once, since we only care about user's stack traces
    if placeholder_node.op == "placeholder":
        users = [to_placeholder_info(i) for i in placeholder_node.users]
        mutating_use_stack_trace = get_mutating_use_stack_trace_from_node(
            placeholder_node
        )

    return PlaceholderInfo(name, stack_trace, users, mutating_use_stack_trace)

