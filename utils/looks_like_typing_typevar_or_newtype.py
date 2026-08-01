
def looks_like_typing_typevar_or_newtype(node) -> bool:
    func = node.func
    if isinstance(func, nodes.Attribute):
        return func.attrname in TYPING_TYPEVARS
    if isinstance(func, nodes.Name):
        return func.name in TYPING_TYPEVARS
    return False

