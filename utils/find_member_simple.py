
def find_member_simple(
    name: str,
    itype: Instance,
    subtype: Type,
    *,
    is_operator: bool = False,
    class_obj: bool = False,
    is_lvalue: bool = False,
) -> Type | None:
    """Find the type of member by 'name' in 'itype's TypeInfo.

    Find the member type after applying type arguments from 'itype', and binding
    'self' to 'subtype'. Return None if member was not found.
    """
    info = itype.type
    method = info.get_method(name)
    if method:
        if isinstance(method, Decorator):
            return find_node_type(method.var, itype, subtype, class_obj=class_obj)
        if method.is_property:
            assert isinstance(method, OverloadedFuncDef)
            dec = method.items[0]
            assert isinstance(dec, Decorator)
            # Pass on is_lvalue flag as this may be a property with different setter type.
            return find_node_type(
                dec.var, itype, subtype, class_obj=class_obj, is_lvalue=is_lvalue
            )
        return find_node_type(method, itype, subtype, class_obj=class_obj)
    else:
        # don't have such method, maybe variable or decorator?
        node = info.get(name)
        v = node.node if node else None
        if isinstance(v, Var):
            return find_node_type(v, itype, subtype, class_obj=class_obj)
        if (
            not v
            and name not in ["__getattr__", "__setattr__", "__getattribute__"]
            and not is_operator
            and not class_obj
            and itype.extra_attrs is None  # skip ModuleType.__getattr__
        ):
            for method_name in ("__getattribute__", "__getattr__"):
                # Normally, mypy assumes that instances that define __getattr__ have all
                # attributes with the corresponding return type. If this will produce
                # many false negatives, then this could be prohibited for
                # structural subtyping.
                method = info.get_method(method_name)
                if method and method.info.fullname != "builtins.object":
                    if isinstance(method, Decorator):
                        getattr_type = get_proper_type(find_node_type(method.var, itype, subtype))
                    else:
                        getattr_type = get_proper_type(find_node_type(method, itype, subtype))
                    if isinstance(getattr_type, CallableType):
                        return getattr_type.ret_type
                    return getattr_type
        if itype.type.fallback_to_any or class_obj and itype.type.meta_fallback_to_any:
            return AnyType(TypeOfAny.special_form)
        if isinstance(v, TypeInfo):
            # PEP 544 doesn't specify anything about such use cases. So we just try
            # to do something meaningful (at least we should not crash).
            return TypeType(fill_typevars_with_any(v))
    if itype.extra_attrs and name in itype.extra_attrs.attrs:
        return itype.extra_attrs.attrs[name]
    return None

