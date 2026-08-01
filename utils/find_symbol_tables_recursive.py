
def find_symbol_tables_recursive(prefix: str, symbols: SymbolTable) -> dict[str, SymbolTable]:
    """Find all nested symbol tables.

    Args:
        prefix: Full name prefix (used for return value keys and to filter result so that
            cross references to other modules aren't included)
        symbols: Root symbol table

    Returns a dictionary from full name to corresponding symbol table.
    """
    result = {prefix: symbols}
    for name, node in symbols.items():
        if isinstance(node.node, TypeInfo) and node.node.fullname.startswith(prefix + "."):
            more = find_symbol_tables_recursive(prefix + "." + name, node.node.names)
            result.update(more)
    return result

