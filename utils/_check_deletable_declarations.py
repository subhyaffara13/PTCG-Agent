
def _check_deletable_declarations(path: str, cdef: ClassDef, ir: ClassIR, errors: Errors) -> None:
    """Validate that attributes listed in __deletable__ refer to definable
    attributes on the class.

    Runs in the prepare phase so we exit early on invalid programs before
    any IR is built.
    """
    if not ir.deletable:
        return
    line = next(
        (
            stmt.line
            for stmt in cdef.info.defn.defs.body
            if isinstance(stmt, AssignmentStmt)
            and isinstance(stmt.lvalues[0], NameExpr)
            and stmt.lvalues[0].name == "__deletable__"
        ),
        cdef.line,
    )
    for attr in ir.deletable:
        if attr not in ir.attributes:
            if not ir.has_attr(attr):
                errors.error(f'Attribute "{attr}" not defined', path, line)
                continue
            for base in ir.mro:
                if attr in base.property_types:
                    errors.error(f'Cannot make property "{attr}" deletable', path, line)
                    break
            else:
                _, base = ir.attr_details(attr)
                errors.error(
                    f'Attribute "{attr}" not defined in "{ir.name}" '
                    f'(defined in "{base.name}")',
                    path,
                    line,
                )

