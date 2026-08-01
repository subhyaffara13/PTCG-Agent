
def get_subscript_const_value(node: nodes.Subscript) -> nodes.Const:
    """Returns the value 'subscript.slice' of a Subscript node.

    :param node: Subscript Node to extract value from
    :returns: Const Node containing subscript value
    :raises InferredTypeError: if the subscript node cannot be inferred as a Const
    """
    inferred = safe_infer(node.slice)
    if not isinstance(inferred, nodes.Const):
        raise InferredTypeError("Subscript.slice cannot be inferred as a nodes.Const")

    return inferred

