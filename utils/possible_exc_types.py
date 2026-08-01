
def possible_exc_types(node: nodes.NodeNG) -> set[nodes.ClassDef]:
    """Gets all the possible raised exception types for the given raise node.

    .. note::

        Caught exception types are ignored.

    :param node: The raise node to find exception types for.

    :returns: A list of exception types possibly raised by :param:`node`.
    """
    exceptions = []
    if isinstance(node.exc, nodes.Name):
        inferred = utils.safe_infer(node.exc)
        if inferred:
            exceptions = [inferred]
    elif node.exc is None:
        handler = node.parent
        while handler and not isinstance(handler, nodes.ExceptHandler):
            handler = handler.parent

        if handler and handler.type:
            try:
                for exception in astroid.unpack_infer(handler.type):
                    if not isinstance(exception, UninferableBase):
                        exceptions.append(exception)
            except astroid.InferenceError:
                pass
    else:
        match target := _get_raise_target(node):
            case nodes.ClassDef():
                exceptions = [target]
            case nodes.FunctionDef():
                for ret in target.nodes_of_class(nodes.Return):
                    if ret.value is None:
                        continue
                    if ret.frame() != target:
                        # return from inner function - ignore it
                        continue

                    val = utils.safe_infer(ret.value)
                    if val and utils.inherit_from_std_ex(val):
                        match val:
                            case nodes.ClassDef():
                                exceptions.append(val)
                            case astroid.Instance():
                                exceptions.append(val.getattr("__class__")[0])

    try:
        return {
            exc
            for exc in exceptions
            if not utils.node_ignores_exception(node, exc.name)
        }
    except astroid.InferenceError:
        return set()

