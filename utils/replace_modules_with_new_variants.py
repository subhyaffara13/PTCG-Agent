
def replace_modules_with_new_variants(
    manager: BuildManager,
    graph: dict[str, State],
    old_modules: dict[str, MypyFile | None],
    new_modules: dict[str, MypyFile | None],
) -> None:
    """Replace modules with newly builds versions.

    Retain the identities of externally visible AST nodes in the
    old ASTs so that references to the affected modules from other
    modules will still be valid (unless something was deleted or
    replaced with an incompatible definition, in which case there
    will be dangling references that will be handled by
    propagate_changes_using_dependencies).
    """
    for id in new_modules:
        preserved_module = old_modules.get(id)
        new_module = new_modules[id]
        if preserved_module and new_module is not None:
            merge_asts(preserved_module, preserved_module.names, new_module, new_module.names)
            manager.modules[id] = preserved_module
            graph[id].tree = preserved_module

