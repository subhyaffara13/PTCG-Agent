
def decorated_with_property(node: nodes.FunctionDef) -> bool:
    """Detect if the given function node is decorated with a property."""
    if not node.decorators:
        return False
    for decorator in node.decorators.nodes:
        try:
            if _is_property_decorator(decorator):
                return True
        except astroid.InferenceError:
            pass
    return False

