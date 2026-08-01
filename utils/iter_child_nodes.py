
def iter_child_nodes(node, omit=None, _fields_order=_FieldsOrder()):
    """
    Yield all direct child nodes of *node*, that is, all fields that
    are nodes and all items of fields that are lists of nodes.

    :param node:          AST node to be iterated upon
    :param omit:          String or tuple of strings denoting the
                          attributes of the node to be omitted from
                          further parsing
    :param _fields_order: Order of AST node fields
    """
    for name in _fields_order[node.__class__]:
        if omit and name in omit:
            continue
        field = getattr(node, name, None)
        if isinstance(field, ast.AST):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, ast.AST):
                    yield item

