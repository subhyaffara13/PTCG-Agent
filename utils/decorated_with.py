
def decorated_with(
    func: (
        nodes.ClassDef | nodes.FunctionDef | astroid.BoundMethod | astroid.UnboundMethod
    ),
    qnames: Iterable[str],
) -> bool:
    """Determine if the `func` node has a decorator with the qualified name `qname`."""
    decorators = func.decorators.nodes if func.decorators else []
    for decorator_node in decorators:
        if isinstance(decorator_node, nodes.Call):
            # We only want to infer the function name
            decorator_node = decorator_node.func
        try:
            if any(
                i.name in qnames or i.qname() in qnames
                for i in decorator_node.infer()
                if isinstance(i, (nodes.ClassDef, nodes.FunctionDef))
            ):
                return True
        except astroid.InferenceError:
            continue
    return False

