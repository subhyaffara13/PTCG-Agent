
def is_generic(t: Type) -> bool:
    t = get_proper_type(t)
    return isinstance(t, Instance) and bool(t.args)

