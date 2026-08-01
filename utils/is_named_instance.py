
def is_named_instance(t: Type, fullnames: str | tuple[str, ...]) -> TypeGuard[Instance]:
    if not isinstance(fullnames, tuple):
        fullnames = (fullnames,)

    t = get_proper_type(t)
    return isinstance(t, Instance) and t.type.fullname in fullnames

