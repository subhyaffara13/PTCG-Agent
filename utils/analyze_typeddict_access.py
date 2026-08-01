
def analyze_typeddict_access(
    name: str, typ: TypedDictType, mx: MemberContext, override_info: TypeInfo | None
) -> Type:
    if name == "__setitem__":
        if isinstance(mx.context, IndexExpr):
            # Since we can get this during `a['key'] = ...`
            # it is safe to assume that the context is `IndexExpr`.
            item_type, key_names = mx.chk.expr_checker.visit_typeddict_index_expr(
                typ, mx.context.index, setitem=True
            )
            assigned_readonly_keys = typ.readonly_keys & key_names
            if assigned_readonly_keys and not mx.suppress_errors:
                mx.msg.readonly_keys_mutated(assigned_readonly_keys, context=mx.context)
        else:
            # It can also be `a.__setitem__(...)` direct call.
            # In this case `item_type` can be `Any`,
            # because we don't have args available yet.
            # TODO: check in `default` plugin that `__setitem__` is correct.
            item_type = AnyType(TypeOfAny.implementation_artifact)
        return CallableType(
            arg_types=[mx.chk.named_type("builtins.str"), item_type],
            arg_kinds=[ARG_POS, ARG_POS],
            arg_names=[None, None],
            ret_type=NoneType(),
            fallback=mx.chk.named_type("builtins.function"),
            name=name,
        )
    elif name == "__delitem__":
        return CallableType(
            arg_types=[mx.chk.named_type("builtins.str")],
            arg_kinds=[ARG_POS],
            arg_names=[None],
            ret_type=NoneType(),
            fallback=mx.chk.named_type("builtins.function"),
            name=name,
        )
    return _analyze_member_access(name, typ.fallback, mx, override_info)

