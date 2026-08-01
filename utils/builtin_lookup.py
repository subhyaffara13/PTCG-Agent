
def builtin_lookup(name: str) -> tuple[nodes.Module, list[nodes.NodeNG]]:
    """Lookup a name in the builtin module.

    Return the list of matching statements and the ast for the builtin module
    """
    manager = AstroidManager()
    try:
        _builtin_astroid = manager.builtins_module
    except KeyError:
        # User manipulated the astroid cache directly! Rebuild everything.
        manager.clear_cache()
        _builtin_astroid = manager.builtins_module
    if name == "__dict__":
        return _builtin_astroid, ()
    try:
        stmts: list[nodes.NodeNG] = _builtin_astroid.locals[name]  # type: ignore[assignment]
    except KeyError:
        stmts = []
    return _builtin_astroid, stmts

