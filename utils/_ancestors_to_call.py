
def _ancestors_to_call(
    klass_node: nodes.ClassDef, method_name: str = "__init__"
) -> dict[nodes.ClassDef, bases.UnboundMethod]:
    """Return a dictionary where keys are the list of base classes providing
    the queried method, and so that should/may be called from the method node.
    """
    to_call: dict[nodes.ClassDef, bases.UnboundMethod] = {}
    for base_node in klass_node.ancestors(recurs=False):
        try:
            init_node = next(base_node.igetattr(method_name))
            if not isinstance(init_node, astroid.UnboundMethod):
                continue
            if init_node.is_abstract():
                continue
            to_call[base_node] = init_node
        except astroid.InferenceError:
            continue
    return to_call

