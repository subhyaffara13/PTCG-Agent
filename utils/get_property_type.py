
def get_property_type(t: ProperType) -> ProperType:
    if isinstance(t, CallableType):
        return get_proper_type(t.ret_type)
    if isinstance(t, Overloaded):
        return get_proper_type(t.items[0].ret_type)
    return t

