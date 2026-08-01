
def paramspec_args(
    name: str,
    fullname: str,
    id: TypeVarId,
    *,
    named_type_func: _NamedTypeCallback,
    line: int = -1,
    column: int = -1,
    prefix: Parameters | None = None,
) -> ParamSpecType:
    return ParamSpecType(
        name,
        fullname,
        id,
        flavor=ParamSpecFlavor.ARGS,
        upper_bound=named_type_func("builtins.tuple", [named_type_func("builtins.object")]),
        default=AnyType(TypeOfAny.from_omitted_generics),
        line=line,
        column=column,
        prefix=prefix,
    )

