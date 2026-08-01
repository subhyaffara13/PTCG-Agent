
def get_module_func_defs(module: MypyFile) -> Iterable[FuncDef]:
    """Collect all of the (non-method) functions declared in a module."""
    for node in module.names.values():
        # We need to filter out functions that are imported or
        # aliases.  The best way to do this seems to be by
        # checking that the fullname matches.
        if isinstance(node.node, (FuncDef, Decorator, OverloadedFuncDef)) and is_from_module(
            node.node, module
        ):
            yield get_func_def(node.node)

