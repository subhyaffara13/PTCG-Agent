
def arg_parser_output_expr(
    arg_index: int, a: PythonArgument, *, symint: bool = True
) -> PythonArgParserOutputExpr:
    has_default = a.default_init is not None
    unpack_method = arg_parser_unpack_method(
        t=a.type, default=a.default, default_init=a.default_init, symint=symint
    )
    default = f", {a.default_init}" if has_default else ""
    expr = f"_r.{unpack_method}({arg_index}{default})"

    return PythonArgParserOutputExpr(
        name=a.name,
        expr=expr,
        index=arg_index,
        argument=a,
    )

