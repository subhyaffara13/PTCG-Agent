
def analyze_descriptor_access(descriptor_type: Type, mx: MemberContext) -> Type:
    """Type check descriptor access.

    Arguments:
        descriptor_type: The type of the descriptor attribute being accessed
            (the type of ``f`` in ``a.f`` when ``f`` is a descriptor).
        mx: The current member access context.
    Return:
        The return type of the appropriate ``__get__/__set__`` overload for the descriptor.
    """
    instance_type = get_proper_type(mx.self_type)
    orig_descriptor_type = descriptor_type
    descriptor_type = get_proper_type(descriptor_type)

    if isinstance(descriptor_type, UnionType):
        # Map the access over union types
        return make_simplified_union(
            [analyze_descriptor_access(typ, mx) for typ in descriptor_type.items]
        )
    elif not isinstance(descriptor_type, Instance):
        return orig_descriptor_type

    if not mx.is_lvalue and not descriptor_type.type.has_readable_member("__get__"):
        return orig_descriptor_type

    # We do this check first to accommodate for descriptors with only __set__ method.
    # If there is no __set__, we type-check that the assigned value matches
    # the return type of __get__. This doesn't match the python semantics,
    # (which allow you to override the descriptor with any value), but preserves
    # the type of accessing the attribute (even after the override).
    if mx.is_lvalue and descriptor_type.type.has_readable_member("__set__"):
        return analyze_descriptor_assign(descriptor_type, mx)

    if mx.is_lvalue and not descriptor_type.type.has_readable_member("__get__"):
        # This turned out to be not a descriptor after all.
        return orig_descriptor_type

    dunder_get = descriptor_type.type.get_method("__get__")
    if dunder_get is None:
        mx.fail(
            message_registry.DESCRIPTOR_GET_NOT_CALLABLE.format(
                descriptor_type.str_with_options(mx.msg.options)
            )
        )
        return AnyType(TypeOfAny.from_error)

    bound_method = analyze_decorator_or_funcbase_access(
        defn=dunder_get,
        itype=descriptor_type,
        name="__get__",
        mx=mx.copy_modified(self_type=descriptor_type),
    )

    typ = map_instance_to_supertype(descriptor_type, dunder_get.info)
    dunder_get_type = expand_type_by_instance(bound_method, typ)

    if isinstance(instance_type, FunctionLike) and instance_type.is_type_obj():
        owner_type = instance_type.items[0].get_instance_type()
        instance_type = NoneType()
    elif isinstance(instance_type, TypeType):
        owner_type = instance_type.item
        instance_type = NoneType()
    else:
        owner_type = instance_type

    callable_name = mx.chk.expr_checker.method_fullname(descriptor_type, "__get__")
    dunder_get_type = mx.chk.expr_checker.transform_callee_type(
        callable_name,
        dunder_get_type,
        [
            TempNode(instance_type, context=mx.context),
            TempNode(TypeType.make_normalized(owner_type), context=mx.context),
        ],
        [ARG_POS, ARG_POS],
        mx.context,
        object_type=descriptor_type,
    )

    _, inferred_dunder_get_type = mx.chk.expr_checker.check_call(
        dunder_get_type,
        [
            TempNode(instance_type, context=mx.context),
            TempNode(TypeType.make_normalized(owner_type), context=mx.context),
        ],
        [ARG_POS, ARG_POS],
        mx.context,
        object_type=descriptor_type,
        callable_name=callable_name,
    )

    # Search for possible deprecations:
    mx.chk.warn_deprecated(dunder_get, mx.context)

    inferred_dunder_get_type = get_proper_type(inferred_dunder_get_type)
    if isinstance(inferred_dunder_get_type, AnyType):
        # check_call failed, and will have reported an error
        return inferred_dunder_get_type

    if not isinstance(inferred_dunder_get_type, CallableType):
        mx.fail(
            message_registry.DESCRIPTOR_GET_NOT_CALLABLE.format(
                descriptor_type.str_with_options(mx.msg.options)
            )
        )
        return AnyType(TypeOfAny.from_error)

    return inferred_dunder_get_type.ret_type

