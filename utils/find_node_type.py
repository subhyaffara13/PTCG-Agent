
def find_node_type(
    node: Var | FuncBase,
    itype: Instance,
    subtype: Type,
    class_obj: bool = False,
    is_lvalue: bool = False,
) -> Type:
    """Find type of a variable or method 'node' (maybe also a decorated method).
    Apply type arguments from 'itype', and bind 'self' to 'subtype'.
    """
    from mypy.typeops import bind_self

    if isinstance(node, FuncBase):
        typ: Type | None = mypy.typeops.function_type(
            node, fallback=Instance(itype.type.mro[-1], [])
        )
    else:
        # This part and the one below are simply copies of the logic from checkmember.py.
        if node.is_settable_property and is_lvalue:
            typ = node.setter_type
            if typ is None and node.is_ready:
                typ = node.type
        else:
            typ = node.type
        if typ is not None:
            typ = expand_self_type(node, typ, subtype)
    p_typ = get_proper_type(typ)
    if typ is None:
        return AnyType(TypeOfAny.from_error)
    # We don't need to bind 'self' for static methods, since there is no 'self'.
    if isinstance(node, FuncBase) or (
        isinstance(p_typ, FunctionLike)
        and node.is_initialized_in_class
        and not node.is_staticmethod
    ):
        assert isinstance(p_typ, FunctionLike)
        if class_obj and not (
            node.is_class if isinstance(node, FuncBase) else node.is_classmethod
        ):
            # Don't bind instance methods on class objects.
            signature = p_typ
        else:
            signature = bind_self(
                p_typ, subtype, is_classmethod=isinstance(node, Var) and node.is_classmethod
            )
        if node.is_property and not class_obj:
            assert isinstance(signature, CallableType)
            if (
                isinstance(node, Var)
                and node.is_settable_property
                and is_lvalue
                and node.setter_type is not None
            ):
                typ = signature.arg_types[0]
            else:
                typ = signature.ret_type
        else:
            typ = signature
    itype = map_instance_to_supertype(itype, node.info)
    typ = expand_type_by_instance(typ, itype)
    return typ

