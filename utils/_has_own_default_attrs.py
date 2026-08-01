
def _has_own_default_attrs(cdef: ClassDef, ir: ClassIR) -> bool:
    """Whether this class's own body has any default attribute assignment
    that would be emitted into __mypyc_defaults_setup.

    Used during prepare to decide whether to register a
    __mypyc_defaults_setup FuncDecl ahead of IR build.
    """
    if ir.builtin_base or ir.is_trait:
        return False
    cls_type = dataclass_type(cdef)
    return any(
        default_attr_name(stmt, ir, cls_type) is not None
        for stmt in cdef.info.defn.defs.body
        if isinstance(stmt, AssignmentStmt)
    )

