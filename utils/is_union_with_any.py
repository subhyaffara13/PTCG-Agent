
def is_union_with_any(tp: Type) -> bool:
    """Is this a union with Any or a plain Any type?"""
    tp = get_proper_type(tp)
    if isinstance(tp, AnyType):
        return True
    if not isinstance(tp, UnionType):
        return False
    return any(is_union_with_any(t) for t in get_proper_types(tp.items))

