
def _attributes_from_assignment(
    ctx: mypy.plugin.ClassDefContext, stmt: AssignmentStmt, auto_attribs: bool, class_kw_only: bool
) -> Iterable[Attribute]:
    """Return Attribute objects that are created by this assignment.

    The assignments can look like this:
        x = attr.ib()
        x = y = attr.ib()
        x, y = attr.ib(), attr.ib()
    or if auto_attribs is enabled also like this:
        x: type
        x: type = default_value
        x: type = attr.ib(...)
    """
    for lvalue in stmt.lvalues:
        lvalues, rvalues = _parse_assignments(lvalue, stmt)

        if len(lvalues) != len(rvalues):
            # This means we have some assignment that isn't 1 to 1.
            # It can't be an attrib.
            continue

        for lhs, rvalue in zip(lvalues, rvalues):
            # Check if the right hand side is a call to an attribute maker.
            if (
                isinstance(rvalue, CallExpr)
                and isinstance(rvalue.callee, RefExpr)
                and rvalue.callee.fullname in attr_attrib_makers
            ):
                attr = _attribute_from_attrib_maker(
                    ctx, auto_attribs, class_kw_only, lhs, rvalue, stmt
                )
                if attr:
                    yield attr
            elif auto_attribs and stmt.type and stmt.new_syntax and not is_class_var(lhs):
                yield _attribute_from_auto_attrib(ctx, class_kw_only, lhs, rvalue, stmt)

