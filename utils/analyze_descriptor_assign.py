
def analyze_descriptor_assign(descriptor_type: Instance, mx: MemberContext) -> Type:
    instance_type = get_proper_type(mx.self_type)
    dunder_set = descriptor_type.type.get_method("__set__")
    if dunder_set is None:
        mx.fail(
            message_registry.DESCRIPTOR_SET_NOT_CALLABLE.format(
                descriptor_type.str_with_options(mx.msg.options)
            ).value
        )
        return AnyType(TypeOfAny.from_error)

    bound_method = analyze_decorator_or_funcbase_access(
        defn=dunder_set,
        itype=descriptor_type,
        name="__set__",
        mx=mx.copy_modified(is_lvalue=False, self_type=descriptor_type),
    )
    typ = map_instance_to_supertype(descriptor_type, dunder_set.info)
    dunder_set_type = expand_type_by_instance(bound_method, typ)

    callable_name = mx.chk.expr_checker.method_fullname(descriptor_type, "__set__")
    rvalue = mx.rvalue or TempNode(AnyType(TypeOfAny.special_form), context=mx.context)
    dunder_set_type = mx.chk.expr_checker.transform_callee_type(
        callable_name,
        dunder_set_type,
        [TempNode(instance_type, context=mx.context), rvalue],
        [ARG_POS, ARG_POS],
        mx.context,
        object_type=descriptor_type,
    )

    # For non-overloaded setters, the result should be type-checked like a regular assignment.
    # Hence, we first only try to infer the type by using the rvalue as type context.
    type_context = rvalue
    with mx.msg.filter_errors():
        _, inferred_dunder_set_type = mx.chk.expr_checker.check_call(
            dunder_set_type,
            [TempNode(instance_type, context=mx.context), type_context],
            [ARG_POS, ARG_POS],
            mx.context,
            object_type=descriptor_type,
            callable_name=callable_name,
        )

    # And now we in fact type check the call, to show errors related to wrong arguments
    # count, etc., replacing the type context for non-overloaded setters only.
    inferred_dunder_set_type = get_proper_type(inferred_dunder_set_type)
    if isinstance(inferred_dunder_set_type, CallableType):
        type_context = TempNode(AnyType(TypeOfAny.special_form), context=mx.context)
    mx.chk.expr_checker.check_call(
        dunder_set_type,
        [TempNode(instance_type, context=mx.context), type_context],
        [ARG_POS, ARG_POS],
        mx.context,
        object_type=descriptor_type,
        callable_name=callable_name,
    )

    # Search for possible deprecations:
    mx.chk.warn_deprecated(dunder_set, mx.context)

    # In the following cases, a message already will have been recorded in check_call.
    if (not isinstance(inferred_dunder_set_type, CallableType)) or (
        len(inferred_dunder_set_type.arg_types) < 2
    ):
        return AnyType(TypeOfAny.from_error)
    return inferred_dunder_set_type.arg_types[1]

