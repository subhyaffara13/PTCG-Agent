
def is_trait(t: t.Any) -> bool:
    """Returns whether the given value is an instance or subclass of TraitType."""
    return isinstance(t, TraitType) or (isinstance(t, type) and issubclass(t, TraitType))


def is_trait(cdef: ClassDef) -> bool:
    return any(is_trait_decorator(d) for d in cdef.decorators) or cdef.info.is_protocol

