
def transform_six_add_metaclass(node):  # pylint: disable=inconsistent-return-statements
    """Check if the given class node is decorated with *six.add_metaclass*.

    If so, inject its argument as the metaclass of the underlying class.
    """
    if not node.decorators:
        return

    for decorator in node.decorators.nodes:
        if not isinstance(decorator, nodes.Call):
            continue

        try:
            func = next(decorator.func.infer())
        except (InferenceError, StopIteration):
            continue
        if (
            isinstance(func, (nodes.FunctionDef, nodes.ClassDef))
            and func.qname() == SIX_ADD_METACLASS
            and decorator.args
        ):
            metaclass = decorator.args[0]
            node._metaclass = metaclass
            return node
    return

