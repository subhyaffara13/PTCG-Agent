
def add_non_ext_class_attr(
    builder: IRBuilder,
    non_ext: NonExtClassInfo,
    lvalue: NameExpr,
    stmt: AssignmentStmt,
    cdef: ClassDef,
    attr_to_cache: list[tuple[Lvalue, RType]],
) -> None:
    """Add a class attribute to __dict__ of a non-extension class."""
    # Only add the attribute to the __dict__ if the assignment is of the form:
    # x: type = value (don't add attributes of the form 'x: type' to the __dict__).
    if not isinstance(stmt.rvalue, TempNode):
        rvalue = builder.accept(stmt.rvalue)
        builder.add_to_non_ext_dict(non_ext, lvalue.name, rvalue, stmt.line)
        # We cache enum attributes to speed up enum attribute lookup since they
        # are final.
        if (
            cdef.info.bases
            # Enum class must be the last parent class.
            and cdef.info.bases[-1].type.is_enum
            # Skip these since Enum will remove it
            and lvalue.name not in EXCLUDED_ENUM_ATTRIBUTES
        ):
            # Enum values are always boxed, so use object_rprimitive.
            attr_to_cache.append((lvalue, object_rprimitive))

