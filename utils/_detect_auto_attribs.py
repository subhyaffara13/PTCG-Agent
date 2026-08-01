
def _detect_auto_attribs(ctx: mypy.plugin.ClassDefContext) -> bool:
    """Return whether auto_attribs should be enabled or disabled.

    It's disabled if there are any unannotated attribs()
    """
    for stmt in ctx.cls.defs.body:
        if isinstance(stmt, AssignmentStmt):
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
                        and not stmt.new_syntax
                    ):
                        # This means we have an attrib without an annotation and so
                        # we can't do auto_attribs=True
                        return False
    return True

