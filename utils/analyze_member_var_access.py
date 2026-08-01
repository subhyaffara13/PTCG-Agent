
def analyze_member_var_access(
    name: str, itype: Instance, info: TypeInfo, mx: MemberContext
) -> Type:
    """Analyse attribute access that does not target a method.

    This is logically part of analyze_member_access and the arguments are similar.

    original_type is the type of E in the expression E.var
    """
    # It was not a method. Try looking up a variable.
    node = info.get(name)
    v = node.node if node else None

    mx.chk.warn_deprecated(v, mx.context)

    vv = v
    is_trivial_self = False
    if isinstance(vv, Decorator):
        # The associated Var node of a decorator contains the type.
        v = vv.var
        is_trivial_self = vv.func.is_trivial_self and not vv.decorators
        if mx.is_super and not mx.suppress_errors:
            validate_super_call(vv.func, mx)
    if isinstance(v, FuncDef):
        assert False, "Did not expect a function"
    if isinstance(v, MypyFile):
        # Special case: accessing module on instances is allowed, but will not
        # be recorded by semantic analyzer.
        mx.chk.module_refs.add(v.fullname)

    if isinstance(vv, (TypeInfo, TypeAlias, MypyFile, TypeVarLikeExpr)):
        # If the associated variable is a TypeInfo synthesize a Var node for
        # the purposes of type checking.  This enables us to type check things
        # like accessing class attributes on an inner class. Similar we allow
        # using qualified type aliases in runtime context. For example:
        #     class C:
        #         A = List[int]
        #     x = C.A() <- this is OK
        typ = mx.chk.expr_checker.analyze_static_reference(vv, mx.context, mx.is_lvalue)
        v = Var(name, type=typ)
        v.info = info

    if isinstance(v, Var):
        implicit = info[name].implicit

        # An assignment to final attribute is always an error,
        # independently of types.
        if mx.is_lvalue and not mx.chk.get_final_context():
            check_final_member(name, info, mx.msg, mx.context)

        return analyze_var(name, v, itype, mx, implicit=implicit, is_trivial_self=is_trivial_self)
    elif (
        not v
        and name not in ["__getattr__", "__setattr__", "__getattribute__"]
        and not mx.is_operator
        and mx.module_symbol_table is None
    ):
        # Above we skip ModuleType.__getattr__ etc. if we have a
        # module symbol table, since the symbol table allows precise
        # checking.
        if not mx.is_lvalue:
            for method_name in ("__getattribute__", "__getattr__"):
                method = info.get_method(method_name)

                # __getattribute__ is defined on builtins.object and returns Any, so without
                # the guard this search will always find object.__getattribute__ and conclude
                # that the attribute exists
                if method and method.info.fullname != "builtins.object":
                    bound_method = analyze_decorator_or_funcbase_access(
                        defn=method, itype=itype, name=method_name, mx=mx
                    )
                    typ = map_instance_to_supertype(itype, method.info)
                    getattr_type = get_proper_type(expand_type_by_instance(bound_method, typ))
                    if isinstance(getattr_type, CallableType):
                        result = getattr_type.ret_type
                    else:
                        result = getattr_type

                    # Call the attribute hook before returning.
                    fullname = f"{method.info.fullname}.{name}"
                    hook = mx.chk.plugin.get_attribute_hook(fullname)
                    if hook:
                        result = hook(
                            AttributeContext(
                                get_proper_type(mx.original_type),
                                result,
                                mx.is_lvalue,
                                mx.context,
                                mx.chk,
                            )
                        )
                    return result
        else:
            setattr_meth = info.get_method("__setattr__")
            if setattr_meth and setattr_meth.info.fullname != "builtins.object":
                bound_type = analyze_decorator_or_funcbase_access(
                    defn=setattr_meth,
                    itype=itype,
                    name="__setattr__",
                    mx=mx.copy_modified(is_lvalue=False),
                )
                typ = map_instance_to_supertype(itype, setattr_meth.info)
                setattr_type = get_proper_type(expand_type_by_instance(bound_type, typ))
                if isinstance(setattr_type, CallableType) and len(setattr_type.arg_types) > 0:
                    return setattr_type.arg_types[-1]

    if itype.type.fallback_to_any:
        return AnyType(TypeOfAny.special_form)

    # Could not find the member.
    if itype.extra_attrs and name in itype.extra_attrs.attrs:
        # For modules use direct symbol table lookup.
        if not itype.extra_attrs.mod_name:
            return itype.extra_attrs.attrs[name]

    if mx.is_super and not mx.suppress_errors:
        mx.msg.undefined_in_superclass(name, mx.context)
        return AnyType(TypeOfAny.from_error)
    else:
        ret = report_missing_attribute(mx.original_type, itype, name, mx)
        # Avoid paying double jeopardy if we can't find the member due to --no-implicit-reexport
        if (
            mx.module_symbol_table is not None
            and name in mx.module_symbol_table
            and not mx.module_symbol_table[name].module_public
        ):
            v = mx.module_symbol_table[name].node
            e = NameExpr(name)
            e.set_line(mx.context)
            e.node = v
            return mx.chk.expr_checker.analyze_ref_expr(e, lvalue=mx.is_lvalue)
        return ret

