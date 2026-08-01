
def arg_parser_output_exprs(
    ps: PythonSignature, f: NativeFunction, *, symint: bool = True
) -> dict[str, PythonArgParserOutputExpr]:
    return {
        e.name: e
        for i, a in enumerate(ps.arguments())
        for e in (arg_parser_output_expr(i, a, symint=symint),)
    }

