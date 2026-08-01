
def cache_class_attrs(
    builder: IRBuilder, attrs_to_cache: list[tuple[Lvalue, RType]], cdef: ClassDef
) -> None:
    """Add class attributes to be cached to the global cache."""
    typ = builder.load_native_type_object(cdef.info.fullname)
    for lval, rtype in attrs_to_cache:
        assert isinstance(lval, NameExpr), lval
        rval = builder.py_get_attr(typ, lval.name, cdef.line)
        builder.init_final_static(lval, rval, cdef.name, type_override=rtype)

