
def analyze_class_attribute_access(
    itype: Instance,
    name: str,
    mx: MemberContext,
    *,
    mcs_fallback: Instance,
    override_info: TypeInfo | None = None,
    original_vars: Sequence[TypeVarLikeType] | None = None,
) -> Type | None:
    """Analyze access to an attribute on a class object.

    itype is the return type of the class object callable, original_type is the type
    of E in the expression E.var, original_vars are type variables of the class callable
    (for generic classes).
    """
    info = itype.type
    if override_info:
        info = override_info

    fullname = f"{info.fullname}.{name}"
    hook = mx.chk.plugin.get_class_attribute_hook(fullname)

    node = info.get(name)
    if not node:
        if itype.extra_attrs and name in itype.extra_attrs.attrs:
            # For modules use direct symbol table lookup.
            if not itype.extra_attrs.mod_name:
                return itype.extra_attrs.attrs[name]
        if info.fallback_to_any or info.meta_fallback_to_any:
            return apply_class_attr_hook(mx, hook, AnyType(TypeOfAny.special_form))
        return None

    if (
        isinstance(node.node, Var)
        and not node.node.is_classvar
        and not hook
        and mcs_fallback.type.get(name)
    ):
        # If the same attribute is declared on the metaclass and the class but with different types,
        # and the attribute on the class is not a ClassVar,
        # the type of the attribute on the metaclass should take priority
        # over the type of the attribute on the class,
        # when the attribute is being accessed from the class object itself.
        #
        # Return `None` here to signify that the name should be looked up
        # on the class object itself rather than the instance.
        return None

    mx.chk.warn_deprecated(node.node, mx.context)

    is_decorated = isinstance(node.node, Decorator)
    is_method = is_decorated or isinstance(node.node, FuncBase)
    if mx.is_lvalue and not mx.suppress_errors:
        if is_method:
            mx.msg.cant_assign_to_method(mx.context)
        if isinstance(node.node, TypeInfo):
            mx.fail(message_registry.CANNOT_ASSIGN_TO_TYPE)

    # Refuse class attribute access if slot defined
    if info.slots and name in info.slots:
        mx.fail(message_registry.CLASS_VAR_CONFLICTS_SLOTS.format(name))

    if node.implicit and isinstance(node.node, Var):
        if node.node.is_final:
            # If a final attribute was declared on `self` in `__init__`, then it
            # can't be accessed on the class object.
            mx.fail(message_registry.CANNOT_ACCESS_FINAL_INSTANCE_ATTR.format(node.node.name))
        elif not mx.is_lvalue and not defined_in_superclass(info, name):
            mx.fail(message_registry.CANNOT_ACCESS_INSTANCE_ONLY_ATTR.format(node.node.name))

    # An assignment to final attribute on class object is also always an error,
    # independently of types.
    if mx.is_lvalue and not mx.chk.get_final_context():
        check_final_member(name, info, mx.msg, mx.context)

    if info.is_enum and not (mx.is_lvalue or is_decorated or is_method):
        enum_class_attribute_type = analyze_enum_class_attribute_access(itype, name, mx)
        if enum_class_attribute_type:
            return apply_class_attr_hook(mx, hook, enum_class_attribute_type)

    t = node.type
    if t:
        if isinstance(t, PartialType):
            symnode = node.node
            assert isinstance(symnode, Var)
            return apply_class_attr_hook(
                mx, hook, mx.chk.handle_partial_var_type(t, mx.is_lvalue, symnode, mx.context)
            )

        # Find the class where method/variable was defined.
        if isinstance(node.node, Decorator):
            super_info: TypeInfo | None = node.node.var.info
        elif isinstance(node.node, (Var, SYMBOL_FUNCBASE_TYPES)):
            super_info = node.node.info
        else:
            super_info = None

        # Map the type to how it would look as a defining class. For example:
        #     class C(Generic[T]): ...
        #     class D(C[Tuple[T, S]]): ...
        #     D[int, str].method()
        # Here itype is D[int, str], isuper is C[Tuple[int, str]].
        if not super_info:
            isuper = None
        else:
            isuper = map_instance_to_supertype(itype, super_info)

        if isinstance(node.node, Var):
            assert isuper is not None
            object_type = get_proper_type(mx.self_type)
            # Check if original variable type has type variables. For example:
            #     class C(Generic[T]):
            #         x: T
            #     C.x  # Error, ambiguous access
            #     C[int].x  # Also an error, since C[int] is same as C at runtime
            # Exception is Self type wrapped in ClassVar, that is safe.
            prohibit_self = not node.node.is_classvar
            def_vars = set(node.node.info.defn.type_vars)
            if prohibit_self and node.node.info.self_type:
                def_vars.add(node.node.info.self_type)
            # Exception: access on Type[...], including first argument of class methods is OK.
            prohibit_generic = not isinstance(object_type, TypeType) or node.implicit
            if prohibit_generic and def_vars & set(get_all_type_vars(t)):
                if node.node.is_classvar:
                    message = message_registry.GENERIC_CLASS_VAR_ACCESS
                else:
                    message = message_registry.GENERIC_INSTANCE_VAR_CLASS_ACCESS
                mx.fail(message)
            t = expand_self_type_if_needed(t, mx, node.node, itype, is_class=True)
            t = expand_type_by_instance(t, isuper)
            # Erase non-mapped variables, but keep mapped ones, even if there is an error.
            # In the above example this means that we infer following types:
            #     C.x -> Any
            #     C[int].x -> int
            if prohibit_generic:
                erase_vars = set(itype.type.defn.type_vars)
                if prohibit_self and itype.type.self_type:
                    erase_vars.add(itype.type.self_type)
                t = erase_typevars(t, {tv.id for tv in erase_vars})

        is_classmethod = (
            (is_decorated and cast(Decorator, node.node).func.is_class)
            or (isinstance(node.node, SYMBOL_FUNCBASE_TYPES) and node.node.is_class)
            or isinstance(node.node, Var)
            and node.node.is_classmethod
        )
        t = get_proper_type(t)
        is_trivial_self = False
        if isinstance(node.node, Decorator):
            # Use fast path if there are trivial decorators like @classmethod or @property
            is_trivial_self = node.node.func.is_trivial_self and not node.node.decorators
        elif isinstance(node.node, (FuncDef, OverloadedFuncDef)):
            is_trivial_self = node.node.is_trivial_self
        if (
            isinstance(t, FunctionLike)
            and is_classmethod
            and not is_trivial_self
            and not t.bound()
        ):
            t = check_self_arg(t, mx.self_type, False, mx.context, name, mx.msg)
        t = add_class_tvars(
            t,
            isuper,
            is_classmethod,
            mx,
            original_vars=original_vars,
            is_trivial_self=is_trivial_self,
        )
        if is_decorated:
            t = expand_self_type_if_needed(
                t, mx, cast(Decorator, node.node).var, itype, is_class=is_classmethod
            )

        result = t
        # __set__ is not called on class objects.
        if not mx.is_lvalue:
            result = analyze_descriptor_access(result, mx)

        return apply_class_attr_hook(mx, hook, result)
    elif isinstance(node.node, Var):
        mx.not_ready_callback(name, mx.context)
        return AnyType(TypeOfAny.special_form)

    if isinstance(node.node, (TypeInfo, TypeAlias, MypyFile, TypeVarLikeExpr)):
        # TODO: should we apply class plugin here (similar to instance access)?
        return mx.chk.expr_checker.analyze_static_reference(node.node, mx.context, mx.is_lvalue)

    if is_decorated:
        assert isinstance(node.node, Decorator)
        if node.node.type:
            return apply_class_attr_hook(mx, hook, node.node.type)
        else:
            mx.not_ready_callback(name, mx.context)
            return AnyType(TypeOfAny.from_error)
    else:
        assert isinstance(node.node, SYMBOL_FUNCBASE_TYPES)
        typ = mx.chk.function_type(node.node)
        # Note: if we are accessing class method on class object, the cls argument is bound.
        # Annotated and/or explicit class methods go through other code paths above, for
        # unannotated implicit class methods we do this here.
        if node.node.is_class:
            typ = bind_self_fast(typ)
        return apply_class_attr_hook(mx, hook, typ)

