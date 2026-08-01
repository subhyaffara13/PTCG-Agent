
def keywords2dict(keywords):
    kwargs = {}
    for node in keywords:
        if isinstance(node, ast.keyword):
            kwargs[node.arg] = node.value
    return kwargs

