
def custom_primitive_op(
    name: str,
    arg_types: list[RType],
    return_type: RType,
    error_kind: int,
    c_function_name: str | None = None,
    var_arg_type: RType | None = None,
    truncated_type: RType | None = None,
    ordering: list[int] | None = None,
    extra_int_constants: list[tuple[int, RType]] | None = None,
    steals: StealsDescription = False,
    is_borrowed: bool = False,
    is_pure: bool = False,
    experimental: bool = False,
    dependencies: list[Dependency] | None = None,
    type_params: list[RTypeVar] | None = None,
) -> PrimitiveDescription:
    """Define a primitive op that can't be automatically generated based on the AST.

    Most arguments are similar to method_op().
    """
    if extra_int_constants is None:
        extra_int_constants = []
    return PrimitiveDescription(
        name=name,
        arg_types=arg_types,
        return_type=return_type,
        var_arg_type=var_arg_type,
        truncated_type=truncated_type,
        c_function_name=c_function_name,
        error_kind=error_kind,
        steals=steals,
        is_borrowed=is_borrowed,
        ordering=ordering,
        extra_int_constants=extra_int_constants,
        priority=0,
        is_pure=is_pure,
        experimental=experimental,
        dependencies=dependencies,
        type_params=type_params,
    )

