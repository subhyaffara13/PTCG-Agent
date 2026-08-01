
def get_expr_length(builder: IRBuilder, expr: Expression) -> int | None:
    folded = constant_fold_expr(builder, expr)
    if isinstance(folded, (str, bytes)):
        return len(folded)
    elif isinstance(expr, (ListExpr, TupleExpr)):
        # if there are no star expressions, or we know the length of them,
        # we know the length of the expression
        stars = [get_expr_length(builder, i) for i in expr.items if isinstance(i, StarExpr)]
        if None not in stars:
            other = sum(not isinstance(i, StarExpr) for i in expr.items)
            return other + sum(stars)  # type: ignore [arg-type]
    elif isinstance(expr, StarExpr):
        return get_expr_length(builder, expr.expr)
    elif (
        isinstance(expr, RefExpr)
        and isinstance(expr.node, Var)
        and expr.node.is_final
        and isinstance(expr.node.final_value, str)
        and expr.node.has_explicit_value
    ):
        return len(expr.node.final_value)
    elif (
        isinstance(expr, CallExpr)
        and isinstance(callee := expr.callee, NameExpr)
        and all(kind == ARG_POS for kind in expr.arg_kinds)
    ):
        fullname = callee.fullname
        if (
            fullname
            in (
                "builtins.list",
                "builtins.tuple",
                "builtins.enumerate",
                "builtins.sorted",
                "builtins.reversed",
            )
            and len(expr.args) == 1
        ):
            return get_expr_length(builder, expr.args[0])
        elif fullname == "builtins.map" and len(expr.args) == 2:
            return get_expr_length(builder, expr.args[1])
        elif fullname == "builtins.zip" and expr.args:
            arg_lengths = [get_expr_length(builder, arg) for arg in expr.args]
            if all(arg is not None for arg in arg_lengths):
                return min(arg_lengths)  # type: ignore [type-var]
        elif fullname == "builtins.range" and len(expr.args) <= 3:
            folded_args = [constant_fold_expr(builder, arg) for arg in expr.args]
            if all(isinstance(arg, int) for arg in folded_args):
                try:
                    return len(range(*cast(list[int], folded_args)))
                except ValueError:  # prevent crash if invalid args
                    pass

    # TODO: extend this, passing length of listcomp and genexp should have worthwhile
    # performance boost and can be (sometimes) figured out pretty easily. set and dict
    # comps *can* be done as well but will need special logic to consider the possibility
    # of key conflicts.

    # we might still be able to get the length directly from the type
    rtype = builder.node_type(expr)
    if isinstance(rtype, RTuple):
        return len(rtype.types)
    return None

