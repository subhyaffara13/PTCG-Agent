
def _is_inside_context_manager(node: nodes.Call) -> bool:
    frame = node.frame()
    if not isinstance(
        frame, (nodes.FunctionDef, astroid.BoundMethod, astroid.UnboundMethod)
    ):
        return False
    return frame.name == "__enter__" or utils.decorated_with(
        frame, "contextlib.contextmanager"
    )

