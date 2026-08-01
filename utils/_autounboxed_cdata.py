
def _autounboxed_cdata(tp: Type) -> ProperType:
    """Get the auto-unboxed version of a CData type, if applicable.

    For *direct* _SimpleCData subclasses, the only type argument of _SimpleCData in the bases list
    is returned.
    For all other CData types, including indirect _SimpleCData subclasses, tp is returned as-is.
    """
    tp = get_proper_type(tp)

    if isinstance(tp, UnionType):
        return make_simplified_union([_autounboxed_cdata(t) for t in tp.items])
    elif isinstance(tp, Instance):
        for base in tp.type.bases:
            if base.type.fullname == "_ctypes._SimpleCData":
                # If tp has _SimpleCData as a direct base class,
                # the auto-unboxed type is the single type argument of the _SimpleCData type.
                assert len(base.args) == 1
                return get_proper_type(base.args[0])
    # If tp is not a concrete type, or if there is no _SimpleCData in the bases,
    # the type is not auto-unboxed.
    return tp

