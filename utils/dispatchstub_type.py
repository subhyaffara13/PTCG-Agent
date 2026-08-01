
def dispatchstub_type(t: Type, *, binds: ArgName) -> NamedCType | None:
    # Dispatch stubs are always plain ints
    r = cpp.valuetype_type(t, binds=binds, symint=False)
    if r is not None:
        return r

    if t == BaseType(BaseTy.Scalar):
        return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
    elif t == BaseType(BaseTy.Tensor):
        return None
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")

