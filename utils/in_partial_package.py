
def in_partial_package(id: str, manager: BuildManager) -> bool:
    """Check if a missing module can potentially be a part of a package.

    This checks if there is any existing parent __init__.pyi stub that
    defines a module-level __getattr__ (a.k.a. partial stub package).
    """
    while "." in id:
        ancestor, _ = id.rsplit(".", 1)
        if ancestor in manager.known_partial_packages:
            return manager.known_partial_packages[ancestor]
        if ancestor in manager.modules:
            ancestor_mod: MypyFile | None = manager.modules[ancestor]
        else:
            # Ancestor is not in build, try quickly if we can find it.
            try:
                ancestor_st = State.new_state(
                    id=ancestor, path=None, source=None, manager=manager, temporary=True
                )
            except (ModuleNotFound, CompileError):
                ancestor_mod = None
            else:
                ancestor_mod = ancestor_st.tree
                # We will not need this anymore.
                ancestor_st.tree = None
        if ancestor_mod is not None:
            # Bail out soon, complete subpackage found
            manager.known_partial_packages[ancestor] = ancestor_mod.is_partial_stub_package
            return ancestor_mod.is_partial_stub_package
        id = ancestor
    return False

