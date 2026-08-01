
def _called_in_methods(
    func: nodes.LocalsDictNodeNG,
    klass: nodes.ClassDef,
    methods: Sequence[str],
) -> bool:
    """Check if the func was called in any of the given methods,
    belonging to the *klass*.

    Returns True if so, False otherwise.
    """
    if not isinstance(func, nodes.FunctionDef):
        return False
    for method in methods:
        try:
            inferred = klass.getattr(method)
        except astroid.NotFoundError:
            continue
        for infer_method in inferred:
            if not isinstance(infer_method, nodes.NodeNG):
                continue
            for call in infer_method.nodes_of_class(nodes.Call):
                try:
                    bound = next(call.func.infer())
                except (astroid.InferenceError, StopIteration):
                    continue
                if not isinstance(bound, astroid.BoundMethod):
                    continue
                func_obj = bound._proxied
                if isinstance(func_obj, astroid.UnboundMethod):
                    func_obj = func_obj._proxied
                if func_obj.name == func.name:
                    return True
    return False

