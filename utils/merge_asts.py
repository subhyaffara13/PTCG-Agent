
def merge_asts(
    old: MypyFile, old_symbols: SymbolTable, new: MypyFile, new_symbols: SymbolTable
) -> None:
    """Merge a new version of a module AST to a previous version.

    The main idea is to preserve the identities of externally visible
    nodes in the old AST (that have a corresponding node in the new AST).
    All old node state (outside identity) will come from the new AST.

    When this returns, 'old' will refer to the merged AST, but 'new_symbols'
    will be the new symbol table. 'new' and 'old_symbols' will no longer be
    valid.
    """
    assert new.fullname == old.fullname
    # Find the mapping from new to old node identities for all nodes
    # whose identities should be preserved.
    replacement_map = replacement_map_from_symbol_table(
        old_symbols, new_symbols, prefix=old.fullname
    )
    # Also replace references to the new MypyFile node.
    replacement_map[new] = old
    # Perform replacements to everywhere within the new AST (not including symbol
    # tables).
    node = replace_nodes_in_ast(new, replacement_map)
    assert node is old
    # Also replace AST node references in the *new* symbol table (we'll
    # continue to use the new symbol table since it has all the new definitions
    # that have no correspondence in the old AST).
    replace_nodes_in_symbol_table(new_symbols, replacement_map)

