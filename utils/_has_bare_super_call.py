
def _has_bare_super_call(fundef_node: nodes.FunctionDef) -> bool:
    for call in fundef_node.nodes_of_class(nodes.Call):
        match call:
            case nodes.Call(func=nodes.Name(name="super"), args=[]):
                return True
    return False

