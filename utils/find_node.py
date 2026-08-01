
def find_node(name: str, info: TypeInfo) -> Var | FuncBase | None:
    """Find the node defining member 'name' in given TypeInfo."""
    # TODO: this code shares some logic with checkmember.py
    method = info.get_method(name)
    if method:
        if isinstance(method, Decorator):
            return method.var
        if method.is_property:
            assert isinstance(method, OverloadedFuncDef)
            dec = method.items[0]
            assert isinstance(dec, Decorator)
            return dec.var
        return method
    else:
        # don't have such method, maybe variable?
        node = info.get(name)
        v = node.node if node else None
        if isinstance(v, Var):
            return v
    return None

