
def _infer_decorator_callchain(node):
    """Detect decorator call chaining and see if the end result is a
    static or a classmethod.
    """
    if not isinstance(node, FunctionDef):
        return None
    if not node.parent:
        return None
    try:
        result = next(node.infer_call_result(node.parent), None)
    except InferenceError:
        return None
    if isinstance(result, bases.Instance):
        result = result._proxied
    if isinstance(result, ClassDef):
        if result.is_subtype_of("builtins.classmethod"):
            return "classmethod"
        if result.is_subtype_of("builtins.staticmethod"):
            return "staticmethod"
    if isinstance(result, FunctionDef):
        if not result.decorators:
            return None
        # Determine if this function is decorated with one of the builtin descriptors we want.
        for decorator in result.decorators.nodes:
            if isinstance(decorator, node_classes.Name):
                if decorator.name in BUILTIN_DESCRIPTORS:
                    return decorator.name
            if (
                isinstance(decorator, node_classes.Attribute)
                and isinstance(decorator.expr, node_classes.Name)
                and decorator.expr.name == "builtins"
                and decorator.attrname in BUILTIN_DESCRIPTORS
            ):
                return decorator.attrname
    return None

