
def _get_use_stack_trace(node: torch.fx.Node) -> str | None:
    for use in node.users:
        if stack_trace := use.meta.get("stack_trace", None):
            return stack_trace
    return None

