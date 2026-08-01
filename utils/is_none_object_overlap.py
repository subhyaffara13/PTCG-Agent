
def is_none_object_overlap(t1: ProperType, t2: ProperType) -> bool:
    return (
        isinstance(t1, NoneType)
        and isinstance(t2, Instance)
        and t2.type.fullname == "builtins.object"
    )

