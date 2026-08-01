
def _build_from_function(
    node: nodes.Module | nodes.ClassDef,
    member: _FunctionTypes,
    module: types.ModuleType,
) -> nodes.FunctionDef | nodes.EmptyNode:
    # verify this is not an imported function
    try:
        code = member.__code__  # type: ignore[union-attr]
    except AttributeError:
        # Some implementations don't provide the code object,
        # such as Jython.
        code = None
    filename = getattr(code, "co_filename", None)
    if filename is None:
        return object_build_methoddescriptor(node, member)
    if filename == getattr(module, "__file__", None):
        return object_build_function(node, member)
    return build_dummy(member)

