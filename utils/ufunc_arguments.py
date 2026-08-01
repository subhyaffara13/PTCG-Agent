
def ufunc_arguments(g: NativeFunctionsGroup, *, compute_t: CType) -> list[Binding]:
    return [
        ufunc_argument(a, compute_t=compute_t)
        for a in g.functional.func.arguments.flat_non_out
    ]

