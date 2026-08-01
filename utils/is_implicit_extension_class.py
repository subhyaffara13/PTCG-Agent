
def is_implicit_extension_class(cdef: ClassDef) -> tuple[bool, str]:
    """Check if class can be extension class and return a user-friendly reason it can't be one."""

    for d in cdef.decorators:
        if (
            not is_trait_decorator(d)
            and not is_dataclass_decorator(d)
            and not get_mypyc_attr_call(d)
            and not is_final_decorator(d)
        ):
            return (
                False,
                "Classes that have decorators other than supported decorators"
                " can't be native classes.",
            )

    if cdef.info.typeddict_type:
        return False, "TypedDict classes can't be native classes."
    if cdef.info.is_named_tuple:
        return False, "NamedTuple classes can't be native classes."
    if cdef.info.metaclass_type and cdef.info.metaclass_type.type.fullname not in (
        "abc.ABCMeta",
        "typing.TypingMeta",
        "typing.GenericMeta",
    ):
        return (
            False,
            "Classes with a metaclass other than ABCMeta, TypingMeta or"
            " GenericMeta can't be native classes.",
        )
    return True, ""

