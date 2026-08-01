
def is_notimplemented_name_node(node):
    return isinstance(node, ast.Name) and getNodeName(node) == 'NotImplemented'

