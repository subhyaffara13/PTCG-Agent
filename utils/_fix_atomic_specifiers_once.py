
def _fix_atomic_specifiers_once(
    decl: c_ast.Decl | c_ast.Typedef,
) -> Tuple[c_ast.Decl | c_ast.Typedef, bool]:
    """Performs one 'fix' round of atomic specifiers.
    Returns (modified_decl, found) where found is True iff a fix was made.
    """
    parent: Any = decl
    grandparent: Any = None
    node: Any = decl.type
    while node is not None:
        if isinstance(node, c_ast.Typename) and "_Atomic" in node.quals:
            break
        try:
            grandparent = parent
            parent = node
            node = node.type
        except AttributeError:
            # If we've reached a node without a `type` field, it means we won't
            # find what we're looking for at this point; give up the search
            # and return the original decl unmodified.
            return decl, False

    assert isinstance(parent, c_ast.TypeDecl)
    assert grandparent is not None
    cast(Any, grandparent).type = node.type
    if "_Atomic" not in node.type.quals:
        node.type.quals.append("_Atomic")
    return decl, True

