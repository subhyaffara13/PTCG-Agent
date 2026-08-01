
def expand_and_bind_callable(
    functype: FunctionLike,
    var: Var,
    itype: Instance,
    name: str,
    mx: MemberContext,
    is_trivial_self: bool,
) -> Type:
    if not mx.preserve_type_var_ids:
        functype = freshen_all_functions_type_vars(functype)
    typ = get_proper_type(expand_self_type(var, functype, mx.self_type))
    assert isinstance(typ, FunctionLike)
    if is_trivial_self:
        typ = bind_self_fast(typ, mx.self_type)
    else:
        typ = check_self_arg(typ, mx.self_type, var.is_classmethod, mx.context, name, mx.msg)
        typ = bind_self(typ, mx.self_type, var.is_classmethod)
    expanded = expand_type_by_instance(typ, itype)
    freeze_all_type_vars(expanded)
    if not var.is_property:
        return expanded
    if isinstance(expanded, Overloaded):
        # Legacy way to store settable properties is with overloads. Also in case it is
        # an actual overloaded property, selecting first item that passed check_self_arg()
        # is a good approximation, long-term we should use check_call() inference below.
        if not expanded.items:
            # A broken overload, error should be already reported.
            return AnyType(TypeOfAny.from_error)
        expanded = expanded.items[0]
    assert isinstance(expanded, CallableType), expanded
    if var.is_settable_property and mx.is_lvalue and var.setter_type is not None:
        if expanded.variables:
            type_ctx = mx.rvalue or TempNode(AnyType(TypeOfAny.special_form), context=mx.context)
            _, inferred_expanded = mx.chk.expr_checker.check_call(
                expanded, [type_ctx], [ARG_POS], mx.context
            )
            expanded = get_proper_type(inferred_expanded)
            assert isinstance(expanded, CallableType)
        if not expanded.arg_types:
            # This can happen when accessing invalid property from its own body,
            # error will be reported elsewhere.
            return AnyType(TypeOfAny.from_error)
        return expanded.arg_types[0]
    else:
        return expanded.ret_type

