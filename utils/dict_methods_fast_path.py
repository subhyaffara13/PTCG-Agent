
def dict_methods_fast_path(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Specialize a common case when list() is called on a dictionary
    view method call.

    For example:
        foo = list(bar.keys())
    """
    if not (len(expr.args) == 1 and expr.arg_kinds == [ARG_POS]):
        return None
    arg = expr.args[0]
    if not (isinstance(arg, CallExpr) and not arg.args and isinstance(arg.callee, MemberExpr)):
        return None
    base = arg.callee.expr
    attr = arg.callee.name
    rtype = builder.node_type(base)
    if not (is_dict_rprimitive(rtype) and attr in ("keys", "values", "items")):
        return None

    obj = builder.accept(base)
    # Note that it is not safe to use fast methods on dict subclasses,
    # so the corresponding helpers in CPy.h fallback to (inlined)
    # generic logic.
    if attr == "keys":
        return builder.call_c(dict_keys_op, [obj], expr.line)
    elif attr == "values":
        return builder.call_c(dict_values_op, [obj], expr.line)
    else:
        return builder.call_c(dict_items_op, [obj], expr.line)

