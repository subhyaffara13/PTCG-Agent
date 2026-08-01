
def get_iterating_dictionary_name(node: nodes.For | nodes.Comprehension) -> str | None:
    """Get the name of the dictionary which keys are being iterated over on
    a ``nodes.For`` or ``nodes.Comprehension`` node.

    If the iterating object is not either the keys method of a dictionary
    or a dictionary itself, this returns None.
    """
    # Is it a proper keys call?
    match node.iter:
        case nodes.Call(func=nodes.Attribute(attrname="keys")):
            inferred = safe_infer(node.iter.func)
            if not isinstance(inferred, astroid.BoundMethod):
                return None
            return node.iter.as_string().rpartition(".keys")[0]  # type: ignore[no-any-return]

    # Is it a dictionary?
    if isinstance(node.iter, (nodes.Name, nodes.Attribute)):
        inferred = safe_infer(node.iter)
        if not isinstance(inferred, nodes.Dict):
            return None
        return node.iter.as_string()  # type: ignore[no-any-return]

    return None

