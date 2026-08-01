
def _lookup_and_create_type(base: type[_T], qname: str) -> _T:
    """
    Given a base type and qualified name: import & lookup that name, check
    that it's of the given type and then instantiate it.
    """
    pkg, name = qname.rsplit(".", 1)
    mod = importlib.import_module(pkg)
    ty = getattr(mod, name)
    if not issubclass(ty, base):
        raise TypeError(f"Type {ty} is not a subtype of {base}")
    return ty()

