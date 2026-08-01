
def is_generic_instance(tp: Type) -> bool:
    tp = get_proper_type(tp)
    return isinstance(tp, Instance) and bool(tp.args)

