
def create_ne_from_eq(builder: IRBuilder, cdef: ClassDef) -> None:
    """Create a "__ne__" method from a "__eq__" method (if only latter exists)."""
    cls = builder.mapper.type_to_ir[cdef.info]
    if cls.has_method("__eq__") and not cls.has_method("__ne__"):
        gen_glue_ne_method(builder, cls, cdef.line)

