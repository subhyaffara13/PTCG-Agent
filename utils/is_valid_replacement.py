
def is_valid_replacement(old: SymbolTableNode, new: SymbolTableNode) -> bool:
    """Can symbol table node replace an existing one?

    These are the only valid cases:

    1. Placeholder gets replaced with a non-placeholder
    2. Placeholder that isn't known to become type replaced with a
       placeholder that can become a type
    """
    if isinstance(old.node, PlaceholderNode):
        if isinstance(new.node, PlaceholderNode):
            return not old.node.becomes_typeinfo and new.node.becomes_typeinfo
        else:
            return True
    return False

