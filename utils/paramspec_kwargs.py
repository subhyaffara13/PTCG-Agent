
def paramspec_kwargs(
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
        flavor=ParamSpecFlavor.KWARGS,
        upper_bound=named_type_func(
            "builtins.dict", [named_type_func("builtins.str"), named_type_func("builtins.object")]
        ),
        default=AnyType(TypeOfAny.from_omitted_generics),
        line=line,
        column=column,
        prefix=prefix,
    )

