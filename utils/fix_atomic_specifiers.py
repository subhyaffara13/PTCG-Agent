
def fix_atomic_specifiers(
    decl: c_ast.Decl | c_ast.Typedef,
) -> c_ast.Decl | c_ast.Typedef:
    """Atomic specifiers like _Atomic(type) are unusually structured,
    conferring a qualifier upon the contained type.

    This function fixes a decl with atomic specifiers to have a sane AST
    structure, by removing spurious Typename->TypeDecl pairs and attaching
    the _Atomic qualifier in the right place.
    """
    # There can be multiple levels of _Atomic in a decl; fix them until a
    # fixed point is reached.
    while True:
        decl, found = _fix_atomic_specifiers_once(decl)
        if not found:
            break

    # Make sure to add an _Atomic qual on the topmost decl if needed. Also
    # restore the declname on the innermost TypeDecl (it gets placed in the
    # wrong place during construction).
    typ: Any = decl
    while not isinstance(typ, c_ast.TypeDecl):
        try:
            typ = typ.type
        except AttributeError:
            return decl
    if "_Atomic" in typ.quals and "_Atomic" not in decl.quals:
        decl.quals.append("_Atomic")
    if typ.declname is None:
        typ.declname = decl.name

    return decl

