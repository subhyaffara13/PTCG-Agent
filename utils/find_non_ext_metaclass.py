
def find_non_ext_metaclass(builder: IRBuilder, cdef: ClassDef, bases: Value) -> Value:
    """Find the metaclass of a class from its defs and bases."""
    if cdef.metaclass:
        declared_metaclass = builder.accept(cdef.metaclass)
    else:
        if cdef.info.typeddict_type is not None:
            # The metaclass for class-based TypedDict is typing._TypedDictMeta.
            # We can't easily calculate it generically, so special case it.
            return builder.get_module_attr("typing", "_TypedDictMeta", cdef.line)
        elif cdef.info.is_named_tuple:
            # The metaclass for class-based NamedTuple is typing.NamedTupleMeta.
            # We can't easily calculate it generically, so special case it.
            return builder.get_module_attr("typing", "NamedTupleMeta", cdef.line)

        declared_metaclass = builder.add(
            LoadAddress(type_object_op.type, type_object_op.src, cdef.line)
        )

    return builder.call_c(py_calc_meta_op, [declared_metaclass, bases], cdef.line)

