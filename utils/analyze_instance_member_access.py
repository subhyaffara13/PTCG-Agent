
def analyze_instance_member_access(
    name: str, typ: Instance, mx: MemberContext, override_info: TypeInfo | None
) -> Type:
    info = typ.type
    if override_info:
        info = override_info

    method = info.get_method(name)

    if name == "__init__" and not mx.is_super and not info.is_final:
        if not method or not method.is_final:
            # Accessing __init__ in statically typed code would compromise
            # type safety unless used via super() or the method/class is final.
            mx.fail(message_registry.CANNOT_ACCESS_INIT)
            return AnyType(TypeOfAny.from_error)

    # The base object has an instance type.

    if (
        state.find_occurrences
        and info.name == state.find_occurrences[0]
        and name == state.find_occurrences[1]
        and not mx.suppress_errors
    ):
        mx.msg.note("Occurrence of '{}.{}'".format(*state.find_occurrences), mx.context)

    # Look up the member. First look up the method dictionary.
    if method and not isinstance(method, Decorator):
        if mx.is_super and not mx.suppress_errors:
            validate_super_call(method, mx)

        if method.is_property:
            assert isinstance(method, OverloadedFuncDef)
            getter = method.items[0]
            assert isinstance(getter, Decorator)
            if mx.is_lvalue and getter.var.is_settable_property:
                mx.chk.warn_deprecated(method.setter, mx.context)
            return analyze_var(name, getter.var, typ, mx)

        if mx.is_lvalue and not mx.suppress_errors:
            mx.msg.cant_assign_to_method(mx.context)
        if not isinstance(method, OverloadedFuncDef):
            signature = mx.chk.function_type(method)
        else:
            if method.type is None:
                # Overloads may be not ready if they are decorated. Handle this in same
                # manner as we would handle a regular decorated function: defer if possible.
                if not mx.no_deferral and method.items:
                    mx.not_ready_callback(method.name, mx.context)
                return AnyType(TypeOfAny.special_form)
            assert isinstance(method.type, Overloaded)
            signature = method.type
        if not mx.preserve_type_var_ids:
            signature = freshen_all_functions_type_vars(signature)
        if not method.is_static:
            if isinstance(method, (FuncDef, OverloadedFuncDef)) and method.is_trivial_self:
                signature = bind_self_fast(signature, mx.self_type)
            else:
                signature = check_self_arg(
                    signature, mx.self_type, method.is_class, mx.context, name, mx.msg
                )
                signature = bind_self(signature, mx.self_type, is_classmethod=method.is_class)
        typ = map_instance_to_supertype(typ, method.info)
        member_type = expand_type_by_instance(signature, typ)
        freeze_all_type_vars(member_type)
        return member_type
    else:
        # Not a method.
        return analyze_member_var_access(name, typ, info, mx)

