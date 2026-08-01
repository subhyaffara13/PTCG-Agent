
def infer_type_sub(node, context: InferenceContext | None = None):
    """
    Infer a type[...] subscript.

    :param node: node to infer
    :type node: astroid.nodes.NodeNG
    :return: the inferred node
    :rtype: nodes.NodeNG
    """
    node_scope, _ = node.scope().lookup("type")
    if not (isinstance(node_scope, nodes.Module) and node_scope.qname() == "builtins"):
        raise UseInferenceDefault()
    class_src = """
    class type:
        def __class_getitem__(cls, key):
            return cls
     """
    node = extract_node(class_src)
    return node.infer(context=context)

