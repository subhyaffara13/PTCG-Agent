
def _attribute_from_auto_attrib(
    ctx: mypy.plugin.ClassDefContext,
    class_kw_only: bool,
    lhs: NameExpr,
    rvalue: Expression,
    stmt: AssignmentStmt,
) -> Attribute:
    """Return an Attribute for a new type assignment."""
    name = unmangle(lhs.name)
    # `x: int` (without equal sign) assigns rvalue to TempNode(AnyType())
    has_rhs = not isinstance(rvalue, TempNode)
    sym = ctx.cls.info.names.get(name)
    init_type = sym.type if sym else None
    return Attribute(name, None, ctx.cls.info, has_rhs, True, class_kw_only, None, stmt, init_type)

