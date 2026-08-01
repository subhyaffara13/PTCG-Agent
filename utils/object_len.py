
def object_len(node, context: InferenceContext | None = None):
    """Infer length of given node object.

    :param Union[nodes.ClassDef, nodes.Instance] node:
    :param node: Node to infer length of

    :raises AstroidTypeError: If an invalid node is returned
        from __len__ method or no __len__ method exists
    :raises InferenceError: If the given node cannot be inferred
        or if multiple nodes are inferred or if the code executed in python
        would result in a infinite recursive check for length
    :rtype int: Integer length of node
    """
    # pylint: disable=import-outside-toplevel; circular import
    from astroid.objects import FrozenSet

    inferred_node = real_safe_infer(node, context=context)

    # prevent self referential length calls from causing a recursion error
    # see https://github.com/pylint-dev/astroid/issues/777
    node_frame = node.frame()
    if (
        isinstance(node_frame, scoped_nodes.FunctionDef)
        and node_frame.name == "__len__"
        and isinstance(inferred_node, bases.Proxy)
        and inferred_node._proxied == node_frame.parent
    ):
        message = (
            "Self referential __len__ function will "
            "cause a RecursionError on line {} of {}".format(
                node.lineno, node.root().file
            )
        )
        raise InferenceError(message)

    if inferred_node is None or isinstance(inferred_node, util.UninferableBase):
        raise InferenceError(node=node)
    if isinstance(inferred_node, nodes.Const) and isinstance(
        inferred_node.value, (bytes, str)
    ):
        return len(inferred_node.value)
    if isinstance(inferred_node, (nodes.List, nodes.Set, nodes.Tuple, FrozenSet)):
        return len(inferred_node.elts)
    if isinstance(inferred_node, nodes.Dict):
        return len(inferred_node.items)

    node_type = object_type(inferred_node, context=context)
    if not node_type:
        raise InferenceError(node=node)

    try:
        len_call = next(node_type.igetattr("__len__", context=context))
    except StopIteration as e:
        raise AstroidTypeError(str(e)) from e
    except AttributeInferenceError as e:
        raise AstroidTypeError(
            f"object of type '{node_type.pytype()}' has no len()"
        ) from e

    inferred = len_call.infer_call_result(node, context)
    if isinstance(inferred, util.UninferableBase):
        raise InferenceError(node=node, context=context)
    result_of_len = next(inferred, None)
    if (
        isinstance(result_of_len, nodes.Const)
        and result_of_len.pytype() == "builtins.int"
    ):
        return result_of_len.value
    if result_of_len is None or (
        isinstance(result_of_len, bases.Instance)
        and result_of_len.is_subtype_of("builtins.int")
    ):
        # Fake a result as we don't know the arguments of the instance call.
        return 0
    raise AstroidTypeError(
        f"'{result_of_len}' object cannot be interpreted as an integer"
    )

