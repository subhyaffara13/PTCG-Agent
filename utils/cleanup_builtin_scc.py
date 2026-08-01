
def cleanup_builtin_scc(state: State) -> None:
    """Remove imported names from builtins namespace.

    This way names imported from typing in builtins.pyi aren't available
    by default (without importing them). We can only do this after processing
    the whole SCC is finished, when the imported names aren't needed for
    processing builtins.pyi itself.
    """
    assert state.tree is not None
    remove_imported_names_from_symtable(state.tree.names, "builtins")

