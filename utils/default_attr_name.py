
def default_attr_name(stmt: AssignmentStmt, ir: ClassIR, cls_type: str | None) -> str | None:
    """Return the attribute name if `stmt` is a class-level default assignment
    that __mypyc_defaults_setup should emit; otherwise None.

    Single source of truth for the predicate used by both
    mypyc.irbuild.classdef.find_attr_initializers (IR build) and
    mypyc.irbuild.prepare._has_own_default_attrs (prepare-phase decl registration).
    """
    lvalue = stmt.lvalues[0]
    if not isinstance(lvalue, NameExpr) or is_class_var(lvalue):
        return None
    if isinstance(stmt.rvalue, TempNode):
        return None
    name = lvalue.name
    if name in ("__slots__", "__deletable__") or name not in ir.attributes:
        return None
    if _defaults_skip(stmt, cls_type):
        return None
    if isinstance(stmt.rvalue, RefExpr) and stmt.rvalue.fullname == "builtins.None":
        attr_type = ir.attributes[name]
        if (
            not is_optional_type(attr_type)
            and not is_object_rprimitive(attr_type)
            and not is_none_rprimitive(attr_type)
        ):
            return None
    return name

