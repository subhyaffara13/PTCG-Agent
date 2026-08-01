
def dataclass_type(cdef: ClassDef) -> str | None:
    for d in cdef.decorators:
        typ = dataclass_decorator_type(d)
        if typ is not None:
            return typ
    return None

