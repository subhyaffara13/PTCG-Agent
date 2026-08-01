
def ufunctor_ctor_argument(a: Argument, scalar_t: BaseCppType) -> Binding:
    return Binding(
        nctype=ufunctor_ctor_type(a.type, binds=a.name, scalar_t=scalar_t),
        name=a.name,
        default=None,
        argument=a,
    )

