
def _clone_node_with_lineno(node, parent, lineno):
    if isinstance(node, nodes.EvaluatedObject):
        node = node.original
    cls = node.__class__
    other_fields = node._other_fields
    _astroid_fields = node._astroid_fields
    init_params = {
        "lineno": lineno,
        "col_offset": node.col_offset,
        "parent": parent,
        "end_lineno": node.end_lineno,
        "end_col_offset": node.end_col_offset,
    }
    postinit_params = {param: getattr(node, param) for param in _astroid_fields}
    if other_fields:
        init_params.update({param: getattr(node, param) for param in other_fields})
    new_node = cls(**init_params)
    if hasattr(node, "postinit") and _astroid_fields:
        new_node.postinit(**postinit_params)
    return new_node

