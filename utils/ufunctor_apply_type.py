
def ufunctor_apply_type(
    t: Type, *, binds: ArgName, scalar_t: BaseCppType
) -> NamedCType:
    if t == BaseType(BaseTy.Tensor):
        return NamedCType(binds, BaseCType(scalar_t))
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")

