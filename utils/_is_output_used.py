
def _is_output_used(
    output_idx: int,
    callers: list[tuple[torch.fx.GraphModule, str, torch.fx.Node]],
) -> bool:
    """Check if output_idx is used by ANY caller (has a getitem with users)."""
    for _parent_gm, _subgraph_name, hop_node in callers:
        for user in hop_node.users:
            if user.op == "call_function" and user.target == operator.getitem:
                if user.args[1] == output_idx and len(user.users) > 0:
                    return True
    return False

