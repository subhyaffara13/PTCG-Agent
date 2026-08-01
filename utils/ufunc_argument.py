
def ufunc_argument(a: Argument, compute_t: CType) -> Binding:
    return Binding(
        nctype=ufunc_type(a.type, binds=a.name, compute_t=compute_t),
        name=a.name,
        default=None,
        argument=a,
    )

