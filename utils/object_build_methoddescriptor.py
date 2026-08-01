
def object_build_methoddescriptor(
    node: nodes.Module | nodes.ClassDef,
    member: _FunctionTypes,
) -> nodes.FunctionDef:
    """create astroid for a living method descriptor object"""
    # FIXME get arguments ?
    name = getattr(member, "__name__", "<no-name>")
    func = build_function(name, node, doc=member.__doc__)
    _add_dunder_class(func, node, member)
    return func

