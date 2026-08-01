
def translate_globals(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) == 0:
        return builder.load_globals_dict()
    return None

