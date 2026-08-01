
def translate_builtins_with_unary_dunder(
    builder: IRBuilder, expr: CallExpr, callee: RefExpr
) -> Value | None:
    """Specialize calls on native classes that implement the associated dunder.

    E.g. i64(x) gets specialized to x.__int__() if x is a native instance.
    """
    if len(expr.args) == 1 and expr.arg_kinds == [ARG_POS] and isinstance(callee, NameExpr):
        arg = expr.args[0]
        arg_typ = builder.node_type(arg)
        shortname = callee.fullname.split(".")[1]
        if shortname in ("i64", "i32", "i16", "u8"):
            method = "__int__"
        else:
            method = f"__{shortname}__"
        if isinstance(arg_typ, RInstance) and arg_typ.class_ir.has_method(method):
            obj = builder.accept(arg)
            return builder.gen_method_call(obj, method, [], None, expr.line)

    return None

