
def find_member(
    name: str,
    itype: Instance,
    subtype: Type,
    *,
    is_operator: bool = False,
    class_obj: bool = False,
    is_lvalue: bool = False,
) -> Type | None:
    type_checker = checker_state.type_checker
    if type_checker is None:
        # Unfortunately, there are many scenarios where someone calls is_subtype() before
        # type checking phase. In this case we fallback to old (incomplete) logic.
        # TODO: reduce number of such cases (e.g. semanal_typeargs, post-semanal plugins).
        return find_member_simple(
            name, itype, subtype, is_operator=is_operator, class_obj=class_obj, is_lvalue=is_lvalue
        )

    # We don't use ATTR_DEFINED error code below (since missing attributes can cause various
    # other error codes), instead we perform quick node lookup with all the fallbacks.
    info = itype.type
    sym = info.get(name)
    node = sym.node if sym else None
    if not node:
        name_not_found = True
        if (
            name not in ["__getattr__", "__setattr__", "__getattribute__"]
            and not is_operator
            and not class_obj
            and itype.extra_attrs is None  # skip ModuleType.__getattr__
        ):
            for method_name in ("__getattribute__", "__getattr__"):
                method = info.get_method(method_name)
                if method and method.info.fullname != "builtins.object":
                    name_not_found = False
                    break
        if name_not_found:
            if info.fallback_to_any or class_obj and info.meta_fallback_to_any:
                return AnyType(TypeOfAny.special_form)
            if itype.extra_attrs and name in itype.extra_attrs.attrs:
                return itype.extra_attrs.attrs[name]
            return None

    from mypy.checkmember import (
        MemberContext,
        analyze_class_attribute_access,
        analyze_instance_member_access,
    )

    mx = MemberContext(
        is_lvalue=is_lvalue,
        is_super=False,
        is_operator=is_operator,
        original_type=TypeType.make_normalized(itype) if class_obj else itype,
        self_type=TypeType.make_normalized(subtype) if class_obj else subtype,
        context=Context(),  # all errors are filtered, but this is a required argument
        chk=type_checker,
        suppress_errors=True,
        # This is needed to avoid infinite recursion in situations involving protocols like
        #     class P(Protocol[T]):
        #         def combine(self, other: P[S]) -> P[Tuple[T, S]]: ...
        # Normally we call freshen_all_functions_type_vars() during attribute access,
        # to avoid type variable id collisions, but for protocols this means we can't
        # use the assumption stack, that will grow indefinitely.
        # TODO: find a cleaner solution that doesn't involve massive perf impact.
        preserve_type_var_ids=True,
    )
    with type_checker.msg.filter_errors(filter_deprecated=True):
        if class_obj:
            fallback = itype.type.metaclass_type or mx.named_type("builtins.type")
            return analyze_class_attribute_access(itype, name, mx, mcs_fallback=fallback)
        else:
            return analyze_instance_member_access(name, itype, mx, info)

