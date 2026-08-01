
def _looks_like_decorated_with_six_add_metaclass(node) -> bool:
    if not node.decorators:
        return False

    for decorator in node.decorators.nodes:
        if not isinstance(decorator, nodes.Call):
            continue
        if decorator.func.as_string() == SIX_ADD_METACLASS:
            return True
    return False

