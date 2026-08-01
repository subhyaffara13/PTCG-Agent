
def is_trivial_bound(tp: ProperType, allow_tuple: bool = False) -> bool:
    if isinstance(tp, Instance) and tp.type.fullname == "builtins.tuple":
        return allow_tuple and is_trivial_bound(get_proper_type(tp.args[0]))
    return isinstance(tp, Instance) and tp.type.fullname == "builtins.object"

