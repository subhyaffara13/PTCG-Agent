
def infer_typing_namedtuple_class(class_node, context: InferenceContext | None = None):
    """Infer a subclass of typing.NamedTuple."""
    # Check if it has the corresponding bases
    annassigns_fields = [
        annassign.target.name
        for annassign in class_node.body
        if isinstance(annassign, nodes.AnnAssign)
    ]
    code = dedent(
        """
    from collections import namedtuple
    namedtuple({typename!r}, {fields!r})
    """
    ).format(typename=class_node.name, fields=",".join(annassigns_fields))
    node = extract_node(code)
    try:
        generated_class_node = next(infer_named_tuple(node, context))
    except StopIteration as e:
        raise InferenceError(node=node, context=context) from e
    for method in class_node.mymethods():
        generated_class_node.locals[method.name] = [method]

    for body_node in class_node.body:
        if isinstance(body_node, nodes.Assign):
            for target in body_node.targets:
                attr = target.name
                generated_class_node.locals[attr] = class_node.locals[attr]
        elif isinstance(body_node, nodes.ClassDef):
            generated_class_node.locals[body_node.name] = [body_node]

    return iter((generated_class_node,))

