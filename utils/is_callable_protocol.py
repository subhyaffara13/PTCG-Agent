
def is_callable_protocol(t: Type) -> bool:
    proper_t = get_proper_type(t)
    if isinstance(proper_t, Instance) and proper_t.type.is_protocol:
        return "__call__" in proper_t.type.protocol_members
    return False

