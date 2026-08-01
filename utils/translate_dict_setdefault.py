
def translate_dict_setdefault(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Special case for 'dict.setdefault' which would only construct
    default empty collection when needed.

    The dict_setdefault_spec_init_op checks whether the dict contains
    the key and would construct the empty collection only once.

    For example, this specializer works for the following cases:
         d.setdefault(key, set()).add(value)
         d.setdefault(key, []).append(value)
         d.setdefault(key, {})[inner_key] = inner_val
    """
    if (
        len(expr.args) == 2
        and expr.arg_kinds == [ARG_POS, ARG_POS]
        and isinstance(callee, MemberExpr)
    ):
        arg = expr.args[1]
        if isinstance(arg, ListExpr):
            if len(arg.items):
                return None
            data_type = Integer(1, c_int_rprimitive, expr.line)
        elif isinstance(arg, DictExpr):
            if len(arg.items):
                return None
            data_type = Integer(2, c_int_rprimitive, expr.line)
        elif (
            isinstance(arg, CallExpr)
            and isinstance(arg.callee, NameExpr)
            and arg.callee.fullname == "builtins.set"
        ):
            if len(arg.args):
                return None
            data_type = Integer(3, c_int_rprimitive, expr.line)
        else:
            return None

        callee_dict = builder.accept(callee.expr)
        key_val = builder.accept(expr.args[0])
        return builder.call_c(
            dict_setdefault_spec_init_op, [callee_dict, key_val, data_type], expr.line
        )
    return None

